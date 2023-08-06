import numpy as np


def px_to_int(pixel_value):
    """Takes a pixel string in the format '123px' and returns the int number."""
    if type(pixel_value) is str:
        pixel_value = int(pixel_value.strip("px"))
    return pixel_value


def make_white_background(height, width):
    """Generate a white background of appropriate height/width and return."""
    white_background = np.zeros([height, width, 3], dtype=np.uint8)
    white_background.fill(255)
    return white_background


def make_transparent_background(height, width):
    """Generate a transparent background of appropriate height/width and return."""
    transparent_background = np.zeros([height, width, 3], dtype=np.uint8)
    return transparent_background


def merge_images(background_image, overlay_image, left, top):
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
