import zipfile

import click
import cv2

from .processor import ManifestHandler


@click.command(help='Get the manifest from a url.')
@click.argument('url')
def build_image_from_manifest(url):

    handler = ManifestHandler()

    final_image = handler.build_image_from_manifest(manifest=url)
    click.echo("Got it!")
    zipf = zipfile.ZipFile('out.zip', 'w', zipfile.ZIP_DEFLATED)
    retval, buf = cv2.imencode('.png', final_image)
    zipf.writestr('final_image.png', buf)
