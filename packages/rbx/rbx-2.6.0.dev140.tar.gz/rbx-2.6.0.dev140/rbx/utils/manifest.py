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
