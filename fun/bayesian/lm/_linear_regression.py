
__all__ = ["LinearRegression"]
from typing import Dict, Literal

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv, cholesky



class LinearRegression:
    def __init__(self, params: Dict = None):
        """
        Parameters:
        - params: Additional parameters as a dictionary. The dictionary can contain the following keys:

            - 'posterior_sample' (int, optional): 
                The number of posterior samples to use for fitting the model. Default is 100.
        """
        if params is None:
            self.params = {}
        else:
            self.params = params
    
    def fit(self, X, y):
        """
        Fit the linear model to the given data.

        Parameters:
        - X: The input features, a 2D array-like object of shape (n_samples, n_features).
        - y: The target values, a 1D array-like object of shape (n_samples,).
        

        Returns:
        - self: The fitted LinearMode object.
        """
        

        n = X.shape[0]
        k = X.shape[1]

        V_beta = inv(X.T @ X)
        beta_hat = V_beta @ X.T @ y
        L = cholesky(V_beta).T
        s2 = np.sum((y - X @ beta_hat)**2) / (n-k)

        # Simulation settings
        M = self.params.get('posterior_sample', 500)
        self.beta_samples = np.zeros((M, k))
        self.sigma2_samples = np.zeros(M)

        for m in range(M):
            self.beta_samples[m] = beta_hat + L @ np.random.normal(size=k)
            self.sigma2_samples[m] = (s2 * (n-k))/np.random.chisquare(n - k)
    

    def coef_(self, mode: Literal['mean', 'mode', 'median'] = 'mean'):
        """
        Get the posterior samples of the coefficients.

        Parameters:
        - mode: The mode for computing the coefficients. Can be one of 'mean', 'mode', or 'median'. Default is 'mean'.
        """

        match mode:
            case 'mean':
                return np.mean(self.beta_samples, axis=0)
            case 'mode':
                return np.mean(self.beta_samples, axis=0)
            case 'median':
                return np.median(self.beta_samples, axis=0)
            case _:
                raise ValueError("Invalid mode. Must be one of 'mean', 'mode', or 'median'.")
    
    def plot_histograms(self):
        num_columns = self.beta_samples.shape[1]
        num_rows = np.ceil(num_columns / 5).astype(int)

        fig, axs = plt.subplots(num_rows, 5, figsize=(20, 4*num_rows), sharey=True)
        fig.suptitle(f'Histograms of beta_samples columns 1 to {num_columns}')
        for i in range(num_rows):
            start = i * 5
            end = (i + 1) * 5

            for j, ax in enumerate(axs[i]):
                if start + j < num_columns:
                    ax.hist(self.beta_samples[:, start + j], bins=50, alpha=0.6)
                    ax.set_title(f'Column {start + j}')
                    ax.set_xlabel('Value')

            axs[i][0].set_ylabel('Frequency')

            plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    """
        Try to run this script to see how to use the LinearRegression class.    
    """
    from sklearn import datasets
    X, y = datasets.load_diabetes(return_X_y=True)
    model = LinearRegression(params = {"posterior_sample": 5000})
    model.fit(X, y)
    print("Coefficients: \n", np.round(model.coef_(), 2))
    model.plot_histograms()

