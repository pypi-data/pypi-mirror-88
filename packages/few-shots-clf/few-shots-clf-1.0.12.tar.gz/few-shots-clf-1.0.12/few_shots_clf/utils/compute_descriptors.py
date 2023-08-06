##########################
# Imports
##########################


from typing import List

import cv2
import numpy as np


##########################
# Function
##########################


def compute_descriptors(img: np.array,
                        keypoints: List[cv2.KeyPoint],
                        feature_descriptor: cv2.Feature2D) -> np.array:
    """Computes the descriptors of the given keypoints on the given image.

    Args:
        img (np.array): The input image.
        keypoints (List[cv2.KeyPoint]): The list of keypoints.
        feature_descriptor (cv2.Feature2D): The feature descriptor to use.

    Returns:
        np.array: The matrix of all descriptors.
    """
    # Extract B, G, R
    img_b = img[:, :, 0]
    img_g = img[:, :, 1]
    img_r = img[:, :, 1]

    # Extract descriptors
    _, descriptors_b = feature_descriptor.compute(img_b, keypoints)
    _, descriptors_g = feature_descriptor.compute(img_g, keypoints)
    _, descriptors_r = feature_descriptor.compute(img_r, keypoints)

    # Concatenate
    descriptors = np.concatenate((descriptors_b,
                                  descriptors_g,
                                  descriptors_r),
                                 axis=-1)

    return descriptors
