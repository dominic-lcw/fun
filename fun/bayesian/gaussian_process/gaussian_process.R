###-------------------------------------------------------------------
### Mean Function
###-------------------------------------------------------------------
m <- function(x){
    10 * x * sin(10 * x)
}

x = seq(0, 1, length.out = 51)
y = m(x)
par(mfrow = c(1,1))
plot(x, y, type = 'l', lwd = 2, cex.axis = 1, cex.lab = 1)


###-------------------------------------------------------------------
### Covariance Function
###-------------------------------------------------------------------
K <- function(x, xprime, ell = 10) {
    
    # Force it to column matrix
    x = matrix(x)
    xprime = matrix(xprime)
   
    # Check how many rows.
    p= dim(x)[1];    
    n= dim(xprime)[1];

    # Broadcast the matrix
    x = matrix(x, nrow = p, ncol = n)
    xprime = matrix(xprime, nrow = n, ncol = p)

    # Compute the kernel
    xprime = t(xprime)
    return(exp(-abs(x - xprime)^2 / ell))
}

# Generate x and y
x = seq(0, 1, length.out = 11) # m = 11
y = seq(0, 1, length.out = 21) # n = 21

# Plot the heatmap without reordering the rows and columns
heatmap(K(x, y), Rowv = NA, Colv = NA)

###-------------------------------------------------------------------
### GP Generation
###-------------------------------------------------------------------
# Continuing above codes
n = 21
x = seq(0, 1, length.out = n)

# Compute Mean
nu = m(x)

# Compute Covariance
S = K(x, x, ell = 1)
jitter = diag(n) * 1e-10 # For numerical stability
A = t(chol(S + jitter))

# Generate Z
nsim = 1000
out = array(NA, dim = c(nsim, n))
for (i in 1:nsim){
    set.seed(i)
    Z = rnorm(n)
    out[i, ] = nu + A %*% Z # One sample

}

par(mfrow = c(1, 2))
# Plot 1: Plotting all the simulated paths
matplot(x, t(out), type = 'l', col = 'dodgerblue', main = 'Simulated Paths')
lines(x, nu, type = 'l', lwd = 3, col = 'black')

# Plot 2: 95% CI
ub = apply(out, 2, function(x) quantile(x, 0.975))
lb = apply(out, 2, function(x) quantile(x, 0.025))
tp_blue = grDevices::adjustcolor("dodgerblue", alpha.f = 0.5)
plot(x, nu, type = 'l', lwd = 3, col = 'black', main = '95% CI')
polygon(c(x, rev(x)), c(lb, rev(ub)), col = tp_blue, border = NA)




