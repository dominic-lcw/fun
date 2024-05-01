import numpy as np
import pandas as pd

from typing import Callable


class EM:

    def __init__(self,
                 n_iter: int = 1000):
        self.n_iter = n_iter

    def load(self, data ,update: Callable):
        self.data = data
        self.update = update
    
    def fit(self, theta0: np.ndarray = None):
        out = np.zeros((self.n_iter, len(theta0)))
        
        for i in range(self.n_iter):
            if i == 0:
                out[i] = self.update(self.data, theta0)
            else:
                out[i] = self.update(self.data, out[i-1])
            if i > 0 and np.sum(np.abs(out[i] - out[i-1])) < 1e-6:
                print("Optimization Succeeded")
                break
        else:
            print("Max Iter Reached")
        return out[:i]
    
        

