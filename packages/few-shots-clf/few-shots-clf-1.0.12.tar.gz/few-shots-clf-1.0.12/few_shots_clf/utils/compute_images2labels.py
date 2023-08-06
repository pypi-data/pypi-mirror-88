##########################
# Imports
##########################


from typing import Dict
from typing import List


##########################
# Function
##########################


def compute_images2labels(images: List[str], labels: List[str]) -> Dict:
    """Maps all image paths to a list of labels.

    Args:
        images (List[str]): The list of image paths.
        labels (List[str]): The list of labels.

    Returns:
        Dict: The mapping between the image paths and the labels.
    """
    # Init images2labels dict
    images2labels = {}

    # Find label for each image
    for image_path in images:
        for label in labels:
            if f"/{label}/" in image_path:
                images2labels[image_path] = label

    return images2labels
