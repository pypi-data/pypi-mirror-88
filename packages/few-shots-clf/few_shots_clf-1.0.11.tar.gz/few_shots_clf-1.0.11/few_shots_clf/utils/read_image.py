##########################
# Imports
##########################


# Global
import cv2
import imutils


##########################
# Function
##########################


def read_image(path, width=None, size=None):
    """[summary]

    Args:
        path ([type]): [description]
        width ([type], optional): [description]. Defaults to None.
        size ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    img = cv2.imread(path)
    if width is not None:
        img = imutils.resize(img, width=width)
    elif size is not None:
        img = cv2.resize(img, (size, size))
    return img
