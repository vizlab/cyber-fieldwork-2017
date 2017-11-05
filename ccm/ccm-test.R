library(rEDM)
library(jsonlite)
library(multispatialCCM)

scalar_fields <- fromJSON("../front/public/data.json")
N_TIMESTEP <- dim(scalar_fields)[1]

a_x <- 50
a_y <- 50
b_x <- 30
b_y <- 30
a_max <- max(scalar_fields[, a_x, a_y])
b_max <- max(scalar_fields[, b_x, b_y])
axis_max <- ifelse(a_max > b_max, a_max, b_max)

a_time_series <- c()
b_time_series <- c()
for (t in 1:N_TIMESTEP) {
  a_time_series <- c(a_time_series, scalar_fields[t, a_x, a_y])
  b_time_series <- c(b_time_series, scalar_fields[t, b_x, b_y])
}


# show data
plot(a_time_series, type="l", col=1, lwd=2, xlim=c(0, N_TIMESTEP), ylim=c(0, axis_max), xlab="time step", ylab="Normalized Value", cex.lab = 1.5)
lines(b_time_series, type="l", col=2, lty=2, lwd=2, cex.lab = 1.5)
legend("bottomright", c("a", "b"), cex=1.5, lty=c(1,2), col=c(1,2), lwd=2, bty="n")


# determine Embedding Dimension
lib <- c(1, 20)
pred <- c(21, 50)  
simplex_output <- simplex(a_time_series, lib, pred)
plot(simplex_output$E, simplex_output$rho, type = "l", xlab = "Embedding Dimension (E)", ylab = "Forecast Skill (rho)")
E_a = 2


lib <- c(1, 20)
pred <- c(21, 50)  
simplex_output <- simplex(b_time_series, lib, pred)
plot(simplex_output$E, simplex_output$rho, type = "l", xlab = "Embedding Dimension (E)", ylab = "Forecast Skill (rho)")
E_b = 2

# create trajectory vector for attractor
E <- 2
TAU <- 1
X_DIM <- E
BACK_MAX <- (X_DIM - 1) * TAU
X_N <- length(a_time_series) - BACK_MAX # length of x
x <- array(0, dim=c(X_N, X_DIM))
for (t in 1 : X_N) {
  for(j in 1:X_DIM) {
    x[t,j] <- a_time_series[(t + BACK_MAX) - (j - 1) * TAU]
  }
}
plot(x, xlim=c(0, 700), ylim=c(0,700), xlab = "x(t)", ylab = "x(t-1)")

# Prediction Decay
simplex_output <- simplex(a_time_series, lib, pred, E = E_a, tp = 1:10)
par(mar = c(4, 4, 1, 1))
plot(simplex_output$tp, simplex_output$rho, type = "l", xlab = "Time to Prediction (tp)", ylab = "Forecast Skill (rho)")

simplex_output <- simplex(b_time_series, lib, pred, E = E_b, tp = 1:10)
par(mar = c(4, 4, 1, 1))
plot(simplex_output$tp, simplex_output$rho, type = "l", xlab = "Time to Prediction (tp)", ylab = "Forecast Skill (rho)")
TAU = 1

# Identifying Nonlinearity
smap_output <- s_map(a_time_series, lib, pred, E = E_a)
par(mar = c(4, 4, 1, 1), mgp = c(2.5, 1, 0))
plot(smap_output$theta, smap_output$rho, type = "l", xlab = "Nonlinearity (theta)", ylab = "Forecast Skill (rho)")

smap_output <- s_map(b_time_series, lib, pred, E = E_b)
par(mar = c(4, 4, 1, 1), mgp = c(2.5, 1, 0))
plot(smap_output$theta, smap_output$rho, type = "l", xlab = "Nonlinearity (theta)", ylab = "Forecast Skill (rho)")

# CCM


