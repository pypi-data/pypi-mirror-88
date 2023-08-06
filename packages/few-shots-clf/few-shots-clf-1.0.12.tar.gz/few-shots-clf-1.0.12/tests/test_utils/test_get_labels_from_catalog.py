##########################
# Imports
##########################


import os
import shutil

from few_shots_clf.utils import get_labels_from_catalog
from tests import empty_dir
from tests import build_catalog
from tests import delete_catalog
from tests.test_utils import TEST_DIRECTORY_PATH


##########################
# Function
##########################


def test_empty_folder():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Get catalog_path
    catalog_path = os.path.join(TEST_DIRECTORY_PATH, "catalog")
    os.makedirs(catalog_path)

    # Get label_path
    label_name = "label"
    label_path = os.path.join(catalog_path, label_name)
    os.makedirs(label_path)

    # Get all labels from catalog
    labels = get_labels_from_catalog(catalog_path)

    # Assert
    assert len(labels) == 0

    # Delete
    shutil.rmtree(label_path)
    shutil.rmtree(catalog_path)
    shutil.rmtree(TEST_DIRECTORY_PATH)


def test_folder_with_no_images():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Get catalog_path
    catalog_path = os.path.join(TEST_DIRECTORY_PATH, "catalog")
    os.makedirs(catalog_path)

    # Get label_path
    label_name = "label"
    label_path = os.path.join(catalog_path, label_name)
    os.makedirs(label_path)

    # Add a file
    file_path = os.path.join(label_path, "tmp.txt")
    with open(file_path, "w") as tmp_file:
        tmp_file.write("test")

    # Get all labels from catalog
    labels = get_labels_from_catalog(catalog_path)

    # Assert
    assert len(labels) == 0

    # Delete
    os.remove(file_path)
    shutil.rmtree(label_path)
    shutil.rmtree(catalog_path)
    shutil.rmtree(TEST_DIRECTORY_PATH)


def test_folder_with_one_label():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Build catalog
    nb_labels = 1
    catalog_path, label_paths, img_paths = build_catalog(TEST_DIRECTORY_PATH,
                                                         nb_labels=nb_labels)

    # Get all labels from catalog
    labels = get_labels_from_catalog(catalog_path)

    # Assert
    assert len(labels) == nb_labels
    for label_path in label_paths:
        label_name = label_path.split("/")[-1]
        assert label_name in labels

    # Delete
    delete_catalog(TEST_DIRECTORY_PATH,
                   catalog_path,
                   label_paths,
                   img_paths)


def test_folder_with_multiple_labels():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Build catalog
    nb_labels = 10
    catalog_path, label_paths, img_paths = build_catalog(TEST_DIRECTORY_PATH,
                                                         nb_labels=nb_labels)

    # Get all labels from catalog
    labels = get_labels_from_catalog(catalog_path)

    # Assert
    assert len(labels) == nb_labels
    for label_path in label_paths:
        label_name = label_path.split("/")[-1]
        assert label_name in labels

    # Delete
    delete_catalog(TEST_DIRECTORY_PATH,
                   catalog_path,
                   label_paths,
                   img_paths)
