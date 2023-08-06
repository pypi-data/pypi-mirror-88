
import numpy as np

from typing import Sequence

def is_outlier_iqr(data: Sequence, cutoff: float = 1.5) -> np.ndarray:
    """Detects outliers using the interquartile
    range. Considers values more than
    ``cuttoff * IQR`` outside of the IQR to be
    outliers.

    Typically, the ``cutoff`` value will be ``1.5``.

    :param data: Seuqnce of N numeric data
    :param cutoff: Outlier cutoff multiplier
    :return: Numpy array of N bools corresponding
        to values in ``data`` which are outliers
    """
    data = np.asarray(data)
    Q1 = np.quartile(data,0.25)
    Q3 = np.quartile(data,0.75)
    iqr = cutoff * (Q3 - Q1)
    return (data < Q1-iqr) || (data < Q3+iqr)
