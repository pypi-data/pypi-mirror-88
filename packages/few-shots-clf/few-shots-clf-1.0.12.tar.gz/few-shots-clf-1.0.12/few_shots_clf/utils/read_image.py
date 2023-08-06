##########################
# Imports
##########################


import cv2
import imutils
import numpy as np


##########################
# Function
##########################


def read_image(path: str, width: int = None, size: int = None) -> np.array:
    """Reads an image given its path.

    Args:
        path (str): Path of the image.
        width (int, optional): Force width to be equal to the given one.
                               Defaults to None.
        size (int, optional): Force width and height of the image to be equal to size.
                              Defaults to None.

    Returns:
        np.array: The image as a numpy array
    """
    img = cv2.imread(path)
    if width is not None:
        img = imutils.resize(img, width=width)
    elif size is not None:
        img = cv2.resize(img, (size, size))
    return img
