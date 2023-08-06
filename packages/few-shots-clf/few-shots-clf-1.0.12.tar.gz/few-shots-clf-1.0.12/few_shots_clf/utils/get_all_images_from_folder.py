##########################
# Imports
##########################


import os
from typing import List

import cv2


##########################
# Function
##########################


def get_all_images_from_folder(path: str) -> List[str]:
    """Lists all image paths contained in a folder.

    Args:
        path (str): The given folder path.

    Returns:
        List[str]: The list of image paths in the folder.
    """
    # Init paths list
    image_paths = []

    # Loop over all sub-folders and sub-files
    for root, _, files in os.walk(path):

        # Loop over all sub-files
        for img_filename in files:
            # Get final file path
            file_path = os.path.join(root, img_filename)

            # Attempt to read image and
            # add its path to the list
            img = cv2.imread(file_path)
            if img is not None:
                image_paths.append(file_path)

    # Sort paths
    image_paths = sorted(image_paths)

    return image_paths
