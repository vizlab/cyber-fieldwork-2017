library(rEDM)
library(jsonlite)
library(multispatialCCM)

data <- fromJSON("./difference-data.json")
f <- data$f
f_t <- data$f_t
f_x <- data$f_x
f_y <- data$f_y
f_tt <- data$f_tt
f_xx <- data$f_xx
f_yy <- data$f_yy

#gradient_fields <- fromJSON("../front/public/gradient-fields.json")
#dx_max <- gradient_fields$x_grad_max
#dy_max <- gradient_fields$y_grad_max
#gradient_fields <- gradient_fields$data
#axis_max <- ifelse(dx_max > dy_max, dx_max, dy_max)

N_TIMESTEP <- dim(f)[1]

a_x <- 10
a_y <- 25

a_time_series <- c()
b_time_series <- c()
for (t in 1:N_TIMESTEP) {
  a_time_series <- c(a_time_series, f_yy[t, a_x, a_y])
  b_time_series <- c(b_time_series, f_xx[t, a_x, a_y])
}

# show data
plot(a_time_series, type="l", col=1, lwd=2)
lines(b_time_series, type="l", col=2, lty=2, lwd=2)
legend("bottomright", c("a", "b"), cex=1.5, lty=c(1,2), col=c(1,2), lwd=2, bty="n")

# determine Embedding Dimension
lib <- c(1, 30)
pred <- c(31, 50)  
simplex_output <- simplex(a_time_series, lib, pred)
plot(simplex_output$E, simplex_output$rho, type = "l", xlab = "Embedding Dimension (E)", ylab = "Forecast Skill (rho)")

simplex_output <- simplex(b_time_series, lib, pred)
plot(simplex_output$E, simplex_output$rho, type = "l", xlab = "Embedding Dimension (E)", ylab = "Forecast Skill (rho)")
E_a <- 2

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
plot(x, xlab = "x(t)", ylab = "x(t-1)")

# Prediction Decay
simplex_output <- simplex(a_time_series, lib, pred, E = E_a, tp = 1:10)
par(mar = c(4, 4, 1, 1))
plot(simplex_output$tp, simplex_output$rho, type = "l", xlab = "Time to Prediction (tp)", ylab = "Forecast Skill (rho)")

simplex_output <- simplex(b_time_series, lib, pred, E = E_a, tp = 1:10)
par(mar = c(4, 4, 1, 1))
plot(simplex_output$tp, simplex_output$rho, type = "l", xlab = "Time to Prediction (tp)", ylab = "Forecast Skill (rho)")
TAU = 5

# Identifying Nonlinearity
smap_output <- s_map(a_time_series, lib, pred, E = E_a)
par(mar = c(4, 4, 1, 1), mgp = c(2.5, 1, 0))
plot(smap_output$theta, smap_output$rho, type = "l", xlab = "Nonlinearity (theta)", ylab = "Forecast Skill (rho)")

smap_output <- s_map(b_time_series, lib, pred, E = E_b)
par(mar = c(4, 4, 1, 1), mgp = c(2.5, 1, 0))
plot(smap_output$theta, smap_output$rho, type = "l", xlab = "Nonlinearity (theta)", ylab = "Forecast Skill (rho)")

# CCM
a_b_dataframe <- data.frame(a=a_time_series, b=b_time_series)
a_xmap_b <- ccm(a_b_dataframe, E = E_a, lib_column = "a", target_column = "b", lib_sizes = seq(10, N_TIMESTEP, by = 5), random_libs = FALSE)
b_xmap_a <- ccm(a_b_dataframe, E = E_a, lib_column = "b", target_column = "a", lib_sizes = seq(10, N_TIMESTEP, by = 5), random_libs = FALSE)

a_xmap_b_means <- ccm_means(a_xmap_b)
b_xmap_a_means <- ccm_means(b_xmap_a)

par(mar = c(4, 4, 1, 1), mgp = c(2.5, 1, 0))
plot(a_xmap_b_means$lib_size, pmax(0, a_xmap_b_means$rho), type = "l", col = "red", xlab = "Library Size", ylab = "Cross Map Skill (rho)", ylim = c(0, 1))
lines(b_xmap_a_means$lib_size, pmax(0, b_xmap_a_means$rho), col = "blue")
legend(x = "topleft", legend = c("a xmap b", "b xmap a"), col = c("red", "blue"), lwd = 1, inset = 0.02, cex = 0.8)

