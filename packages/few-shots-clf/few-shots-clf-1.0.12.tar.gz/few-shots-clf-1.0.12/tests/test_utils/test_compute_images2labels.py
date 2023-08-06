##########################
# Imports
##########################


from few_shots_clf.utils import compute_images2labels


##########################
# Function
##########################


def test_empty_lists():
    """[summary]
    """
    # Get images and labels
    images = []
    labels = []

    # Get images2labels
    images2labels = compute_images2labels(images, labels)

    # Assert
    assert len(images2labels.keys()) == 0
    assert len(images2labels.values()) == 0
    assert images2labels == {}


def test_empty_images():
    """[summary]
    """
    # Get images and labels
    images = [f"/{i}/test.png"
              for i in range(10)]
    labels = []

    # Get images2labels
    images2labels = compute_images2labels(images, labels)

    # Assert
    assert images2labels == {}


def test_empty_labels():
    """[summary]
    """
    # Get images and labels
    images = []
    labels = [f"{i}"
              for i in range(10)]

    # Get images2labels
    images2labels = compute_images2labels(images, labels)

    # Assert
    assert images2labels == {}


def test_equals_images_and_labels():
    """[summary]
    """
    # Get images and labels
    images = [f"/{i}/test.png"
              for i in range(10)]
    labels = [f"{i}"
              for i in range(10)]

    # Get images2labels
    images2labels = compute_images2labels(images, labels)

    # Get true images2labels
    real_images2labels = {images[i]: labels[i]
                          for i in range(10)}

    # Assert
    assert images2labels == real_images2labels


def test_more_images_than_labels():
    """[summary]
    """
    # Get images and labels
    images = [f"/{i}/test_{j}.png"
              for i in range(10)
              for j in range(10)]
    labels = [f"{i}" for i in range(10)]

    # Get images2labels
    images2labels = compute_images2labels(images, labels)

    # Get true images2labels
    real_images2labels = {images[i * 10 + j]: labels[i]
                          for i in range(10)
                          for j in range(10)}

    print(real_images2labels)

    # Assert
    assert images2labels == real_images2labels
