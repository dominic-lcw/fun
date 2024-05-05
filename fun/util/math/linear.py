from typing import List, Union

import numpy as np

def column_vector(v: Union[List, np.ndarray]) -> np.ndarray:
    return np.array(v).reshape(-1, 1)

def column_indicator(A: np.ndarray) -> np.ndarray:
    """ A is the event in column vector """
    return A.astype(int)

def inner_product(v1: np.ndarray, v2: np.ndarray, rminf = True) -> np.ndarray:
    if rminf:
        v1 = np.where(np.isinf(v1), 0, v1)
        v2 = np.where(np.isinf(v2), 0, v2)
    return np.dot(v1.T, v2)

