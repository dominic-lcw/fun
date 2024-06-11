import numpy as np
import numpy.linalg as la
import numpy.random as rng
import matplotlib.pyplot as plt

# Example 8.1: Multiple linear regression
np.random.seed(1)
n = 100
p = 5
beta = np.arange(1, p+1).reshape(-1, 1)
sigma = 0.5
X = np.hstack((np.ones((n, 1)), np.random.standard_t(5, size=(n, p-1))))
Y = X @ beta + np.random.normal(scale=sigma, size=(n, 1))
X_names = [f"X{i+1}" for i in range(p)]
Y_names = ["Y"]
data = np.hstack((Y, X))
print(data[:3, :])

# Function for generating MVN sample
def rMVN(n, Mu, Sigma):
    Mu = np.array(Mu)
    Sigma = np.array(Sigma)
    d = len(Mu)
    E = la.eig(Sigma)
    D = E[0]
    Q = E[1]
    SigmaSqrt = Q @ np.diag(np.sqrt(D)) @ la.inv(Q)
    return (Mu + SigmaSqrt @ np.random.randn(d, n)).T

# Gibbs sampler
def Gibbs(J):
    theta = np.empty((J+1, p+1))
    theta_names = [f"beta{i+1}" for i in range(p)] + ["sigma2"]
    theta[0] = np.concatenate((np.random.normal(size=p), np.random.exponential()))
    for j in range(1, J+1):
        # update beta
        A = la.inv(Sigma) + X.T @ X / theta[j-1, p]
        B = la.inv(Sigma) @ Mu + X.T @ Y / theta[j-1, p]
        theta[j, :p] = rMVN(1, la.inv(A) @ B, la.inv(A))
        # update sigma2
        SSE = np.sum((Y - X @ theta[j, :p])**2)
        theta[j, p] = 1 / rng.gamma((n+p)/2, 1/(SSE/2 + b))
    return theta

# Linear regression Example
np.random.seed(1)
a = 1
b = 1
Mu = np.zeros((p, 1))
Sigma = np.eye(p)

J = 2**12
JBurn = int(J * 0.5)
theta = Gibbs(J)
thetaUse = theta[JBurn+1:]
print(np.mean(thetaUse, axis=0))
print(np.var(thetaUse, axis=0))

# Plotting
plt.figure()
for i in range(p+1):
    plt.subplot(p+1, 1, i+1)
    plt.plot(thetaUse[:, i])
    # plt.ylabel(theta_names[i])
plt.xlabel("Iteration")
plt.tight_layout()
plt.show()
