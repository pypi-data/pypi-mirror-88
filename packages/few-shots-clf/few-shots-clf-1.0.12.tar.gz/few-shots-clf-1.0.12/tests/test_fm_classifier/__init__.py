# pylint: disable=no-member

##########################
# Imports
##########################


import os

import cv2
from easydict import EasyDict as edict

from tests import TEST_DIRECTORY_PATH as DIR_PATH


##########################
# Constants
##########################


TEST_DIRECTORY_PATH = os.path.join(DIR_PATH, "test_fm_classifier")


##########################
# Functions
##########################


def build_config():
    """[summary]
    """
    config = edict({
        "verbose": True,
        "feature_descriptor": cv2.xfeatures2d.SURF_create(extended=True),
        "feature_dimension": 128 * 3,
        "image_size": 256,
        "keypoint_stride": 8,
        "keypoint_sizes": [12, 24, 32, 48, 56, 64],
        "matcher_path": os.path.join(TEST_DIRECTORY_PATH, "matcher-classifier-custom.ann"),
        "matcher_distance": "angular",
        "matcher_n_trees": 10,
        "scoring": "count",
        "k_nn": 1,
        "fingerprint_path": os.path.join(TEST_DIRECTORY_PATH, "fingerprint.pickle")
    })
    return config
