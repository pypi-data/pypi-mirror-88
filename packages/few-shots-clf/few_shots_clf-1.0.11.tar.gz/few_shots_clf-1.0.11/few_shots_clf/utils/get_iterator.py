
##########################
# Imports
##########################


# Global
from tqdm import tqdm


##########################
# Function
##########################


def get_iterator(iterator, verbose=True, description=""):
    """[summary]

    Args:
        iterator ([type]): [description]
        verbose (bool, optional): [description]. Defaults to True.
        description (str, optional): [description]. Defaults to "".

    Returns:
        [type]: [description]
    """
    if verbose:
        iterator = tqdm(iterator, desc=description)
    return iterator
