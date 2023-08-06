##########################
# Imports
##########################


from typing import List

import cv2
import numpy as np


##########################
# Function
##########################


def compute_keypoints(img: np.array, kpt_stride: int, kpt_sizes: List[int]) -> List[cv2.KeyPoint]:
    """Computes evenly-spaced keypoints from a given image.

    Args:
        img (np.array): The input image.
        kpt_stride (int): The stride (spacing) between the keypoints.
        kpt_sizes (List[int]): A list of keypoint sizes.

    Returns:
        List[cv2.KeyPoint]: The list of all keypoints.
    """
    # Init keypoints
    keypoints = []

    # Loop over size
    for size in kpt_sizes:
        # Loop over x
        for x_coord in range(0, img.shape[1], kpt_stride):
            # Loop over y
            for y_coord in range(0, img.shape[0], kpt_stride):
                kpt = cv2.KeyPoint(x_coord, y_coord, size)
                keypoints.append(kpt)

    return keypoints
