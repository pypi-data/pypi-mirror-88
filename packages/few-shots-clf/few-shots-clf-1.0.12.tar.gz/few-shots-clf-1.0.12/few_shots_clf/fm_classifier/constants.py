# pylint: disable=no-member

##########################
# Imports
##########################


import os
import cv2


##########################
# Constants
##########################


VERBOSE = True  # boolean (True or False)

FEATURE_DESCRIPTOR = cv2.xfeatures2d.SURF_create(extended=True)

FEATURE_DIMENSION = 128 * 3

IMAGE_SIZE = 256  # int

KEYPOINT_STRIDE = 8  # int

KEYPOINT_SIZES = [12, 24, 32, 48, 56, 64]  # List of ints

TMP_FOLDER_PATH = "/tmp/few_shots_clf/fm_classifier/"  # existing path

MATCHER_PATH = os.path.join(TMP_FOLDER_PATH,
                            "matcher-classifier-custom.ann")

MATCHER_DISTANCE = "angular"

MATCHER_N_TREES = 10

FINGERPRINT_PATH = os.path.join(TMP_FOLDER_PATH,
                                "fingerprint.pickle")

SCORING = "count"  # Can be "distance" or "count"

K_NN = 1
