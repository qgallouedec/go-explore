from typing import Optional

import numpy as np


def indexes(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Indexes of a in b.

    :param a: Array of shape (...)
    :param b: Array of shape (N x ...)
    :return: Indexes of the occurences of a in b
    """
    if b.shape[0] == 0:
        return np.array([])
    a = a.flatten()
    b = b.reshape((b.shape[0], -1))
    idxs = np.where((a == b).all(1))[0]
    return idxs


def index(a: np.ndarray, b: np.ndarray) -> Optional[int]:
    """
    Index of first occurence of a in b.

    :param a: Array of shape (...)
    :param b: Array of shape (N x ...)
    :return: index of the first occurence of a in b
    """
    idxs = indexes(a, b)
    if idxs.shape[0] == 0:
        return None
    else:
        return idxs[0]


def multinomial(weights: np.ndarray) -> int:
    p = weights / weights.sum()
    r = np.random.multinomial(1, p, size=1)
    idx = np.nonzero(r)[1][0]
    return idx


def sample_geometric(mean: int, max_value: int) -> int:
    """
    Geometric sampling with some modifications.

    (1) The sampled value is < max_value.
    (2) The mean cannot be below max_value/20.
        If it is the case, the mean is replaced by max_value/20.

    :param mean: Mean of the geometric distribution
    :param max_value: Maximum value for the sample
    :return: Sampled value
    """
    # Clip the mean by 1/20th of the max value
    mean = np.clip(mean, a_min=int(max_value / 20), a_max=None)
    while True:  # loop until a correct value is found
        # for a geometric distributon, p = 1/mean
        value = np.random.geometric(1 / mean)
        if value < max_value:
            return value
