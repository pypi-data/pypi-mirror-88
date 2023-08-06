##########################
# Imports
##########################


import os
import shutil

from few_shots_clf.utils import get_all_images_from_folder
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

    # Get all images from folder
    paths = get_all_images_from_folder(TEST_DIRECTORY_PATH)

    # Assert
    assert len(paths) == 0


def test_folder_with_no_images():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Add a file
    file_path = os.path.join(TEST_DIRECTORY_PATH, "tmp.txt")
    with open(file_path, "w") as tmp_file:
        tmp_file.write("test")

    # Get all images from folder
    paths = get_all_images_from_folder(TEST_DIRECTORY_PATH)

    # Assert
    assert len(paths) == 0

    # Delete
    os.remove(file_path)
    shutil.rmtree(TEST_DIRECTORY_PATH)


def test_folder_with_multiple_images():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Build catalog
    catalog_path, label_paths, img_paths = build_catalog(TEST_DIRECTORY_PATH)

    # Get all images from folder
    paths = get_all_images_from_folder(TEST_DIRECTORY_PATH)

    # Assert
    assert len(paths) == len(img_paths)
    for img_path in img_paths:
        assert img_path in paths

    # Delete
    delete_catalog(TEST_DIRECTORY_PATH,
                   catalog_path,
                   label_paths,
                   img_paths)
