##########################
# Imports
##########################


from tqdm import tqdm

from few_shots_clf.utils import get_iterator


##########################
# Function
##########################


def test_no_verbose():
    """[summary]
    """
    # List
    test_list = range(10)

    # Get iterator
    iterator = get_iterator(test_list,
                            verbose=False)

    # Assert
    assert isinstance(iterator, type(test_list))


def test_verbose():
    """[summary]
    """
    # List
    test_list = range(10)

    # Get iterator
    iterator = get_iterator(test_list,
                            verbose=True)

    # Assert
    assert isinstance(iterator, tqdm)


def test_with_description():
    """[summary]
    """
    # List
    test_list = range(10)

    # Description
    test_description = "Test Description"

    # Get iterator
    iterator = get_iterator(test_list,
                            verbose=True,
                            description=test_description)

    # Assert
    assert iterator.desc == test_description
