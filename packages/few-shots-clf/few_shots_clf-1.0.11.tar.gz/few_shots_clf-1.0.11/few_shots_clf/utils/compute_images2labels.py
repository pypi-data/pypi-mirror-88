##########################
# Function
##########################


def compute_images2labels(images, labels):
    """[summary]

    Args:
        images ([type]): [description]
        labels ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Init images2labels dict
    images2labels = {}

    # Find label for each image
    for image_path in images:
        for label in labels:
            if f"/{label}/" in image_path:
                images2labels[image_path] = label

    return images2labels
