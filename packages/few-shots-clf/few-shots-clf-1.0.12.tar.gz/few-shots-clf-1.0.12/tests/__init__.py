##########################
# Imports
##########################


import os
import shutil

import cv2
import numpy as np


##########################
# Constants
##########################


TEST_DIRECTORY_PATH = "/tmp/test_few_shots_clf"


##########################
# Functions
##########################


def empty_dir(dir_path):
    """[summary]
    """
    # Empty dir
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

    # Create dir
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def build_catalog(dir_path, nb_labels=10, nb_images_per_label=None):
    """[summary]

    Args:
        dir_path ([type]): [description]
        nb_labels (int, optional): [description]. Defaults to 10.

    Returns:
        [type]: [description]
    """
    # Create catalog_path
    catalog_path = os.path.join(dir_path, "catalog")
    os.makedirs(catalog_path)

    # Get labels_paths
    label_names = [f"label{k}"
                   for k in range(nb_labels)]
    label_paths = [os.path.join(catalog_path, label_name)
                   for label_name in label_names]
    for label_path in label_paths:
        os.makedirs(label_path)

    # Loop over label_paths
    img_paths = []
    for label_path in label_paths:
        # Get nb_images
        if nb_images_per_label is None:
            nb_images = np.random.randint(1, 5)
        else:
            nb_images = nb_images_per_label

        # Create images
        for k in range(nb_images):
            # Create image
            img = np.zeros((10, 10, 3))

            # Save image
            img_path = os.path.join(label_path, f"tmp{k}.jpg")
            cv2.imwrite(img_path, img)

            # Update img_paths list
            img_paths.append(img_path)

    return catalog_path, label_paths, img_paths


def delete_catalog(dir_path, catalog_path, label_paths, image_paths):
    """[summary]

    Args:
        dir_path ([type]): [description]
        catalog_path ([type]): [description]
        label_paths ([type]): [description]
        image_paths ([type]): [description]
    """
    # Remove images
    for image_path in image_paths:
        os.remove(image_path)

    # Remove labels
    for label_path in label_paths:
        shutil.rmtree(label_path)

    # Remove catalog
    shutil.rmtree(catalog_path)

    # Remove dir
    shutil.rmtree(dir_path)
