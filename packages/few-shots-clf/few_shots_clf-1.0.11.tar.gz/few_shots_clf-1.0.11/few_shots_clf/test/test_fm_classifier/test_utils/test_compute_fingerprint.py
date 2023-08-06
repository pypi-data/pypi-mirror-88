##########################
# Imports
##########################


# Local
from few_shots_clf.test import empty_dir
from few_shots_clf.test import build_catalog
from few_shots_clf.test import delete_catalog
from few_shots_clf.test.test_fm_classifier import build_config
from few_shots_clf.fm_classifier.utils import compute_fingerprint
from few_shots_clf.test.test_fm_classifier.test_utils import TEST_DIRECTORY_PATH


##########################
# Function
##########################


def test_compute_fingerprint():
    """[summary]
    """
    # Empty dir
    empty_dir(TEST_DIRECTORY_PATH)

    # Build catalog
    catalog_path, label_paths, img_paths = build_catalog(TEST_DIRECTORY_PATH,
                                                         nb_labels=10,
                                                         nb_images_per_label=2)

    # Build config
    config = build_config()

    # Compute fingerprint
    fingerprint = compute_fingerprint(catalog_path, config)

    # Assert
    print(fingerprint)
    assert fingerprint == "6b314882d97623aabeeda9310f073d893201a341ad5844078dd46f73"

    # Delete catalog
    delete_catalog(TEST_DIRECTORY_PATH,
                   catalog_path,
                   label_paths,
                   img_paths)
