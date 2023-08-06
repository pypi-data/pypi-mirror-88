##########################
# Imports
##########################


# Built-in
from hashlib import sha224

# Global
import cv2
import numpy as np

# Local
from few_shots_clf.utils import get_all_images_from_folder
from few_shots_clf.utils import get_iterator


##########################
# Function
##########################


def compute_fingerprint(catalog_path, config):
    """[summary]

    Args:
        catalog_path ([type]): [description]
        config ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Catalog fingerprint
    catalog_fingerprint = _compute_catalog_fingerprint(catalog_path,
                                                       verbose=config.verbose)

    # Config fingerprint
    config_fingerprint = _compute_config_fingerprint(config)

    # Final fingerprint
    fingerprint = f"{catalog_fingerprint}{config_fingerprint}"
    fingerprint = sha224(str.encode(fingerprint)).hexdigest()

    return fingerprint


def _compute_catalog_fingerprint(catalog_path, verbose=True):
    # Init. catalog fingerprint
    catalog_fingerprint = ""

    # Get all paths
    image_paths = get_all_images_from_folder(catalog_path)

    # Iterator
    iterator = get_iterator(
        image_paths,
        verbose=verbose,
        description="Computing fingerprint...")

    # Loop over image_paths
    for image_path in iterator:
        # Hash image_path
        path_hash = sha224(str.encode(image_path)).hexdigest()

        # Read image
        img = cv2.imread(image_path)

        # Convert image to string
        img_str = np.array2string(img)

        # Hash image
        img_hash = sha224(str.encode(img_str)).hexdigest()

        # Compute image_fingerprint
        image_fingerprint = f"{path_hash}{img_hash}"

        # Update catalog_fingerprint
        catalog_fingerprint = f"{catalog_fingerprint}{image_fingerprint}"

    # Compute final fingerprint
    catalog_fingerprint = sha224(str.encode(catalog_fingerprint)).hexdigest()

    return catalog_fingerprint


def _compute_config_fingerprint(config):
    # Init config fingerprint
    config_fingerprint = ""

    # Add feature_descriptor
    config_fingerprint = f"{config_fingerprint}{str(config.feature_descriptor.getDefaultName())}"

    # Add feature_dimension
    config_fingerprint = f"{config_fingerprint}{config.feature_dimension}"

    # Add image_size
    config_fingerprint = f"{config_fingerprint}{config.image_size}"

    # Add keypoint_stride
    config_fingerprint = f"{config_fingerprint}{config.keypoint_stride}"

    # Add keypoint_sizes
    config_fingerprint = f"{config_fingerprint}{str(config.keypoint_sizes)}"

    # Add matcher_distance
    config_fingerprint = f"{config_fingerprint}{config.matcher_distance}"

    # Add matcher_n_trees
    config_fingerprint = f"{config_fingerprint}{config.matcher_n_trees}"

    return config_fingerprint
