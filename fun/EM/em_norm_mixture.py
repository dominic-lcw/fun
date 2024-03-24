import numpy as np
from scipy.stats import norm


def get_tau( y, mu0, mu1, sigma0 = 1, sigma1 = 1, p = 1/2):
    phi0 = norm.pdf(y, mu0, sigma0)
    phi1 = norm.pdf(y, mu1, sigma1) 
    
    x =  phi1 * p / (phi1 * p + phi0 * (1-p))
    return x

def update_em(y, theta_n):
    mu0_j, mu1_j, sigma0, sigma1, p = theta_n
    
    tau = get_tau(y, mu0_j, mu1_j, sigma0, sigma1, p)
    
    mu0_jp1 = np.sum(y * (1 - tau))/ np.sum( 1-tau )
    mu1_jp1 = np.sum( tau * y) / np.sum(tau )
    
    return (mu0_jp1, mu1_jp1, sigma0, sigma1, p)