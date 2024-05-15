"""
   lm
   ========== 
   Linear Models

"""

__all__ = ["LinearRegression"]

import numpy as np
from numpy.linalg import inv, cholesky

from typing import Dict

class LinearRegression:
    def __init__(self, param: Dict = None):
        """
        Parameters:
        - param: Additional parameters as a dictionary. The dictionary can contain the following keys:

            - 'posterior_sample' (int, optional): 
                The number of posterior samples to use for fitting the model. Default is 100.
        """
        if param is None:
            param = {}
        # Access the parameters from the dictionary
        M = param.get('posterior_sample', 100)
        self.coefficients = None
    
    def fit(self, X, y):
        """
        Fit the linear model to the given data.

        Parameters:
        - X: The input features, a 2D array-like object of shape (n_samples, n_features).
        - y: The target values, a 1D array-like object of shape (n_samples,).
        

        Returns:
        - self: The fitted LinearModel object.
        """
        

        n = X.shape[0]
        k = X.shape[1]

        V_beta = inv(X.T @ X)
        beta_hat = V_beta @ X.T @ y
        L = cholesky(V_beta).T
        s2 = np.sum((y - X @ beta_hat)**2) / (X.shape[0] - X.shape[1])

        self.beta_samples = np.zeros((M, k))
        self.sigma_samples = np.zeros(M)

        for m in range(M):
            self.beta_samples[m] = beta_hat + L @ np.random.normal(size=k)
            self.sigma_samples[m] = (s2 * (n-k))/np.random.chisquare(n - k)
        


