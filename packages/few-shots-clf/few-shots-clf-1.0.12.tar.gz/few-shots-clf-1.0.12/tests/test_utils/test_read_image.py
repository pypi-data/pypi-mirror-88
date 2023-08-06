##########################
# Imports
##########################


import os
import shutil

import cv2
import numpy as np

from few_shots_clf.utils import read_image
from tests import empty_dir
from tests.test_utils import TEST_DIRECTORY_PATH


##########################
# Function
##########################


def test_fixed_size():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Create image
    img_h = np.random.randint(10, 100)
    img_w = np.random.randint(10, 100)
    img = np.zeros((img_h, img_w, 3))

    # Save image
    img_path = os.path.join(TEST_DIRECTORY_PATH, "tmp.jpg")
    cv2.imwrite(img_path, img)

    # Resize img
    resized_img = read_image(img_path, size=50)
    resized_h, resized_w, _ = resized_img.shape

    # Assert
    assert resized_w == 50
    assert resized_h == 50

    # Delete
    os.remove(img_path)
    shutil.rmtree(TEST_DIRECTORY_PATH)


def test_fixed_width():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Create image
    img_h = np.random.randint(10, 100)
    img_w = np.random.randint(10, 100)
    img = np.zeros((img_h, img_w, 3))

    # Save image
    img_path = os.path.join(TEST_DIRECTORY_PATH, "tmp.jpg")
    cv2.imwrite(img_path, img)

    # Resize img
    resized_img = read_image(img_path, width=50)
    resized_h, resized_w, _ = resized_img.shape

    # Assert
    assert resized_w == 50
    assert resized_h == int(50 * img_h / img_w)

    # Delete
    os.remove(img_path)
    shutil.rmtree(TEST_DIRECTORY_PATH)
