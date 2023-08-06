##########################
# Imports
##########################


# Local
from .get_all_images_from_folder import get_all_images_from_folder


##########################
# Function
##########################


def get_labels_from_catalog(catalog_path):
    """[summary]

    Args:
        catalog_path ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Get all images paths
    image_paths = get_all_images_from_folder(catalog_path)

    # Remove catalog path from image paths
    image_paths_without_catalog = list(map(lambda path: path.replace(catalog_path, ""),
                                           image_paths))

    # Remove leaf file
    image_paths_without_leaf_file = list(map(lambda path: "_".join(path.split("/")[:-1]),
                                             image_paths_without_catalog))

    # Get unique labels
    labels = list(set(image_paths_without_leaf_file))

    # Remove "_" at the beginning and at the end
    labels = map(lambda label: label[1:] if label[0] == "_" else label,
                 labels)
    labels = map(lambda label: label[:-1] if label[-1] == "_" else label,
                 labels)

    # Sort labels
    labels = sorted(labels)

    return labels
