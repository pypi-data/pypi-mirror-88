
import numpy as np

def ln(d: np.ndarray):
    """
    """
    return np.log(d)

def logE(d: np.ndarray):
    """
    """
    return np.log(d)

def log2(d: np.ndarray):
    """
    """
    return np.log2(d)

def log10(d: np.ndarray):
    """
    """
    return np.log10(d)

def sqrt(d: np.ndarray):
    """
    """
    return np.sqrt(d)

def box_cox(d: np.ndarray, lambda_=1.0):
    """
    """
    if lambda_ == 0: return np.log(d)
    else: return (np.power(d,lambda_)-1) / lambda_
