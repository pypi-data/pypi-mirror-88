##########################
# Imports
##########################


from typing import Iterable

from tqdm import tqdm


##########################
# Function
##########################


def get_iterator(iterator: Iterable, verbose: bool = True, description: str = "") -> Iterable:
    """Turns a given iterator into a tqdm iterator when verbose is True.

    Args:
        iterator (Iterable): The given iterator.
        verbose (bool, optional): True to turn the iterator into a tqdm one.
                                  Defaults to True.
        description (str, optional): The description of the tqdm iterator.
                                     Defaults to "".

    Returns:
        Iterable: The iterator tqdmed (or not depending on the verbose variable).
    """
    if verbose:
        iterator = tqdm(iterator, desc=description)
    return iterator
