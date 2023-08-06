##########################
# Imports
##########################


# Built-in
import os

# Global
import cv2


##########################
# Function
##########################


def get_all_images_from_folder(path):
    """[summary]

    Args:
        path ([type]): [description]

    Returns:
        [type]: [description]
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
