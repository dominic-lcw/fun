#### Section 1: Data Loading ####

## Data Download, this will create a file in your directory.
# download.file("http://www.mechanicalkern.com/static/birthdates-1968-1988.csv", "./birthdates-1968-1988.csv")

## Load the data.
df = read.csv("./birthdates-1968-1988.csv")
print(names(df))
df$dates <- as.Date(paste(df$year, df$month, df$day, sep = "-"))


####------------------------------------------------####
#### Section 2: Data Plotting ####
####------------------------------------------------####
## In particular, we only look at 1 to n
par(mfrow = c(1, 1))
n = 100
plot(df$dates[0:n], df$births[0:n], type = 'l', 
    ylim = c(0, max(df$births)*1.5), lwd = 2)

t = c(1:30, 40:45, 60:83, 90:100)
tprime = t
y = df$births[t]

####------------------------------------------------####
#### Section 2: Fitting a Kernel (with only time t) ####
####------------------------------------------------####
kernel.1 <- function(x, xprime, tau = 1, ell = 10) {
    # Input:
    #   x: px1
    #   xprime: nx1
    # Output: 
    #   p*n matrix.
    # The majority of the code is just handling dimensions
    #    for multiple scenarios.

    x.dim = dim(x)
    xprime.dim = dim(xprime)        

    # Fixing Dimensions
    # If null, convert to column vector
    if(is.null(x.dim)){
        x = matrix(x)
        x.dim = dim(x)
    }
    if(is.null(xprime.dim)){
        xprime = matrix(xprime)
        xprime.dim = dim(xprime)
    } 
    # Check how many rows.
    p= x.dim[1];    
    n= xprime.dim[1];

    # We broadcast the matrix
    x = matrix(x, nrow = p, ncol = n)
    xprime = matrix(xprime, nrow = n, ncol = p)

    # Compute the kernel
    xprime = t(xprime)
    return(tau^2 * exp(-abs(x - xprime)^2 / ell))
}


# Why is the below formula, 
#   please refer to conditional multivaraite-normal distribution.
sigma = 0.05
tau.1 = 1  ## Kernel Variance
ell.1 = 30  ## Kernel Bandwidth

# Configure the Plotting Layout
layout.matrix = matrix(c(1, 2,
                         3, 4,
                         5, 6), ncol = 2, byrow = T)
layout(mat = layout.matrix, width = c(2, 0.5))
par(mar = c(4.5, 5, 3, 2),
    cex.axis = 2, 
    cex.lab = 2,
    cex.main = 2)


fitted.kernel = solve(kernel.1(t, t, tau.1, ell.1) + sigma * diag(length(t))) 
# Plot Variance
x.new = 1:100
y.new = kernel.1(x.new, t, tau=tau.1, ell=ell.1)%*%fitted.kernel %*%y

plot(t, y, 
    type = 'l', col = 'black', lwd = 2,
    ylim = c(0, max(y)*1.5),
    main = paste("Fitted GP (Sigma: ", sigma, ", Tau: ", tau.1, ", Ell: ", ell.1,")"))
lines(x.new, y.new , type = 'l', lwd = 2, col = 'red')


par(mar = c(0, 1, 0, 5))
plot(0, type = 'n', axes = F, ann = F)
legend("center", legend = c("Y", "Y.hat"), col = c("black", "red"), 
        lty = 1, 
        cex = 1.5,
        bty = 'n')


####--------------------------------------------------####
#### Section 2a: Fitting a Kernel (varying Sigma) ####
####--------------------------------------------------####

### Varying Sigma
par(mar = c(4.5, 5, 3, 2),
    cex.axis = 2, 
    cex.lab = 2,
    cex.main = 2)
colors = c("goldenrod", "goldenrod1",
            "dodgerblue1", "dodgerblue2", "dodgerblue3", "dodgerblue4")
sigma.all = c(0.01, 0.05, seq(0.1, 1, by = 0.3))

for (i in 1:length(sigma.all) ) {
    sigma = sigma.all[i]
    fitted.kernel = solve(kernel.1(t, t, tau.1, ell.1) + sigma * diag(length(t))) 
    x.new = 1:100
    y.new = kernel.1(x.new, t, tau=tau.1, ell=ell.1)%*%fitted.kernel %*%y
    if(i == 1){
        plot(t, y, 
        type = 'l', col = 'black', lwd = 2,
        ylim = c(0, max(y)*1.5),
        main = paste("Fitted GP (Varying Sigma)"))
        lines(x.new, y.new , type = 'l', lwd = 2, col = colors[i])
    } else {
        lines(x.new, y.new , type = 'l', lwd = 2, col = colors[i])
    }

}

par(mar = c(0, 1, 0, 5))
plot(0, type = 'n', axes = F, ann = F)
legend("center", legend = paste("Sigma: ", sigma.all), col = colors, 
        lty = 1, 
        cex = 1.5,
        title = 'Sigma',
        bty = 'n')


####--------------------------------------------------####
#### Section 2b: Fitting a Kernel (varying Bandwidth) ####
####--------------------------------------------------####

### Varying ell (bandwidth)
par(mar = c(4.5, 5, 3, 2),
    cex.axis = 2, 
    cex.lab = 2,
    cex.main = 2)
colors = c("goldenrod", "goldenrod1",
            "dodgerblue1", "dodgerblue2", "dodgerblue3", "dodgerblue4")
ell.all = c(1, 2, seq(5, 25, by = 5))
sigma = 0.1
for (i in 1:length(ell.all) ) {
    ell.1 = ell.all[i]
    fitted.kernel = solve(kernel.1(t, t, tau.1, ell.1) + sigma * diag(length(t))) 
    x.new = 1:100
    y.new = kernel.1(x.new, t, tau=tau.1, ell=ell.1)%*%fitted.kernel %*%y
    if(i == 1){
        plot(t, y, 
        type = 'l', col = 'black', lwd = 2,
        ylim = c(0, max(y)*1.5),
        main = paste("Fitted GP (Varying Ell)"))
        lines(x.new, y.new , type = 'l', lwd = 2, col = colors[i])
    } else {
        lines(x.new, y.new , type = 'l', lwd = 2, col = colors[i])
    }

}

par(mar = c(0, 1, 0, 5))
plot(0, type = 'n', axes = F, ann = F)
legend("center", legend = paste("Ell: ", ell.all), col = colors, 
        lty = 1, 
        cex = 1.5,
        title = 'Ell',
        bty = 'n')





















