
import numpy as np

from typing import Sequence


def min_max_scale(data: Sequence) -> np.ndarray:
    """Rescale data to the range [0,1]

    :param data: Sequence of numeric data
    :return: ``data`` rescaled to the range [0,1]
    """
    data = np.asarray(data)
    min_, max_ = np.min(data), np.max(data)
    return (data - min_) / (max_ - min_)

def standardize(data: Sequence) -> np.ndarray:
    """Rescale data to have a mean value of ``0.0``
    and a standard deviation of ``1.0``.

    :param data: Sequence of numeric data
    :return: ``data`` rescaled to have (mean=0,std=1)
    """
    data = np.asarray(data)
    mean = np.mean(data)
    std = np.std(data)
    return (data - mean) / std

def l2_norm(data: Sequence) -> np.ndarray:
    """

    :param data: Sequence of numeric data
    :return:
    """
    data = np.asarray(data)
    mag = np.sqrt(np.sum(data * data))
    return data / mag
