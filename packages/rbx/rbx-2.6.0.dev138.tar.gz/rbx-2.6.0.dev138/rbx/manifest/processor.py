import json
from collections import defaultdict

import cv2
import numpy as np

from .aws import S3Bucket
from ..utils.manifest import px_to_int, make_white_background, make_transparent_background
from ..exceptions import FatalException
from ..settings import AWS_BUCKET


class ManifestHandler:

    def __init__(self):
        self.bucket = AWS_BUCKET
        self.client = S3Bucket(name=self.bucket)

    def build_image_from_manifest(self, manifest):
        """Given the AWS URL of a manifest, generate the image creative and write to file."""

        # retrieve the manifest from S3
        manifest = self.get_manifest(manifest)

        # get the root component from the manifest, then make white canvas for all elements to be
        # applied to
        root = manifest.get('root_component')
        root_image = make_white_background(
            height=px_to_int(root['css']['height']),
            width=px_to_int(root['css']['width'])
        )

        # build all elements within the root_component tree
        built_image = self.build_component(
            component=root,
            height=px_to_int(root['css']['height']),
            width=px_to_int(root['css']['width'])
        )

        # merge the final image generated from the root_component tree with the initial canvas
        final_image = _merge_images(
            background_image=root_image,
            overlay_image=built_image,
            left=px_to_int(root['css']['left']),
            top=px_to_int(root['css']['top']),
        )

        return final_image

    def build_component(self, component, height, width):
        """Takes manifest and the height/width of underlying canvas this component will be
        applied to.

        Returns the compiled image.
        """
        images = defaultdict(list)
        layer = component.get('component_manifests', [])
        for element in layer:
            element_dict = {
                    'left': px_to_int(element['css']['left']),
                    'top': px_to_int(element['css']['top']),
                }
            # if the component is a layout, then we need to build the images within the layout
            # before proceeding
            if element['component_type'] == 'layout':
                element_dict['image'] = self.build_component(
                    component=element,
                    height=px_to_int(element['css']['height']),
                    width=px_to_int(element['css']['width'])
                )
            # otherwise, retrieve the image from AWS
            elif element['component_type'] == 'image':
                element_dict['image'] = self.get_image(
                    url=element.get('url'),
                    ext=element.get('ext')
                )
            # add the image details to the corresponding z-index list (this is a list instead of a
            # unique dict entry in case the z-index is duplicated)
            images[element['css']['z-index']].append(element_dict)

        # these images won't all necessarily overlap cleanly, so we need a transparent layer to
        # stick them to
        composite_image = make_transparent_background(height, width)
        # now we can apply all the images, starting with the lowest z-index and increasing
        for key, z_index_layer in sorted(images.items()):
            for entry in z_index_layer:
                _merge_images(
                    background_image=composite_image,
                    overlay_image=entry.get('image'),
                    left=px_to_int(entry.get('left')),
                    top=px_to_int(entry.get('top')),
                )
        return composite_image

    def get_image(self, url, ext):
        """Retrieve Image from S3 and return."""
        image = self.client.get_key('{}{}'.format(url, ext))
        if image is None:
            raise FatalException(
                message="Image Not Found At Specified URL: {}/{}{}".format(self.bucket, url, ext),
                details='{}{}'.format(url, ext)
            )
        img_data = image.get()['Body'].read()
        decoded_image = cv2.imdecode(np.asarray(bytearray(img_data)), cv2.IMREAD_UNCHANGED)

        return decoded_image

    def get_manifest(self, url):
        """Retrieve Manifest from S3 and return."""
        manifest_data = self.client.get_key(url)
        if manifest_data is None:
            raise FatalException(
                "Manifest Not Found At Specified URL: {}/{}".format(self.bucket, url)
            )
        try:
            file_content = manifest_data.get()['Body'].read()
            manifest = json.loads(file_content)
        except UnicodeDecodeError:
            raise FatalException("Manifest has an invalid format: {}".format(url))

        return manifest


def _merge_images(background_image, overlay_image, left, top):
    """Puts the overlay image on top of the background image.

    Will use the left and top to calculate the position of the overlay image relative to the
    background image. Any transparency the top image has will be applied, showing the background
    image where applicable.
    """
    try:
        # reposition overlay image
        y1, y2 = top, top + overlay_image.shape[0]
        x1, x2 = left, left + overlay_image.shape[1]

        # blend alpha channels
        alpha_s = overlay_image[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        # apply overlay image to background image
        for c in range(0, 3):
            background_image[y1:y2, x1:x2, c] = (
                alpha_s * overlay_image[:, :, c] + alpha_l * background_image[y1:y2, x1:x2, c]
            )

    except IndexError:
        # if there is no alpha channel, the process of overlapping images is different
        background_image[
            top:top + overlay_image.shape[0], left:left + overlay_image.shape[1]
        ] = overlay_image

    return background_image
