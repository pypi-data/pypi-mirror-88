##########################
# Imports
##########################


import numpy as np


##########################
# Function
##########################


def compute_descriptors(img, keypoints, feature_descriptor):
    """[summary]

    Args:
        img ([type]): [description]
        keypoints ([type]): [description]
        feature_descriptor ([type]): [description]

    Returns:
        [type]: [description]
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
