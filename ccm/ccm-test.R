library(rEDM)
library(jsonlite)
library(multispatialCCM)

showdata <- function(Accm, Bccm) {
  plot(Accm, type="l", col=1, lwd=2, xlim=c(0, 212), ylim=c(0,1), xlab="time step", ylab="Normalized Value", cex.lab = 1.5)
  lines(Bccm, type="l", col=2, lty=2, lwd=2, cex.lab = 1.5)
  legend("topleft", c("Salinity", "Temprature"), cex=1.5, lty=c(1,2), col=c(1,2), lwd=2, bty="n")
}

determineEmbeddingDimension <- function(data) {
  lib <- c(1, 50)
  pred <- c(90, 212)  
  simplex_output <- simplex(data, lib, pred)
  plot(simplex_output$E, simplex_output$rho, type = "l", xlab = "Embedding Dimension (E)", ylab = "Forecast Skill (rho)")
}

predictionDeacy <- function(data, Em) {
  lib <- c(1, 50)
  pred <- c(90, 212)  
  simplex_output <- simplex(data, lib, pred, E = Em, tp = 1:10)
  par(mar = c(4, 4, 1, 1))
  plot(simplex_output$tp, simplex_output$rho, type = "l", xlab = "Time to Prediction (tp)", ylab = "Forecast Skill (rho)")
}

identifyingNonlinearity <- function(data, Em) {
  lib <- c(1, 50)
  pred <- c(90, 212)  
  smap_output <- s_map(data, lib, pred, E=E_A)
  par(mar = c(4, 4, 1, 1), mgp = c(2.5, 1, 0))
  plot(smap_output$theta, smap_output$rho, type = "l", xlab = "Nonlinearity (theta)", ylab = "Forecast Skill (rho)")
}

drawCCM <- function(CCM_boot_A, CCM_boot_B) {
  plotxlimits<-range(c(CCM_boot_A$Lobs, CCM_boot_B$Lobs))
  plot(CCM_boot_A$Lobs, CCM_boot_A$rho, type="l", col=1, lwd=2, xlim=c(plotxlimits[1], plotxlimits[2]), ylim=c(0,1), xlab="Library Size", ylab="Cross Map Skill (rho)", cex.lab = 1.5)
  lines(CCM_boot_B$Lobs, CCM_boot_B$rho, type="l", col=2, lty=2, lwd=2)
  legend("topleft", c("Salinity causes Temprature", "Temprature causes Salinituy"), lty=c(1,2), col=c(1,2), lwd=2, bty="n", cex=1.2)
}

scalar_fields <- fromJSON("../front/public/data.json")
N_TIMESTEP <- dim(scalar_fields)[1]

a_x <- 50
a_y <- 50
b_x <- 30
b_y <- 30
a_time_series <- c()
b_time_series <- c()
for (t in 1:N_TIMESTEP) {
  a_time_series <- c(a_time_series, scalar_fields[t, a_y, a_x])
  b_time_series <- c(b_time_series, scalar_fields[t, b_y, b_x])
}
plot(a_time_series)
plot(b_time_series)

# show data
showdata(Accm, Bccm)
# determine Embedding Dimension
determineEmbeddingDimension(a_time_series)
E_A = 2
determineEmbeddingDimension(Bccm)
E_B = 2
# Prediction Decay
predictionDeacy(data = Accm, Em = E_A)
predictionDeacy(data = Bccm, Em = E_B)
TAU = 1
# Identifying Nonlinearity
identifyingNonlinearity(data = Accm, Em = E_A)
identifyingNonlinearity(data = Bccm, Em = E_B)
# CCM(use multispatialCCM)
signal_A_out<-SSR_check_signal(A=Accm, E=E_A, tau=TAU, predsteplist=1:10)
signal_B_out<-SSR_check_signal(A=Bccm, E=E_B, tau=TAU, predsteplist=1:10)
CCM_boot_A<-CCM_boot(Accm, Bccm, E_A, tau=TAU, iterations=30)
CCM_boot_B<-CCM_boot(Bccm, Accm, E_B, tau=TAU, iterations=30)
(CCM_significance_test<-ccmtest(CCM_boot_A, CCM_boot_B))
drawCCM(CCM_boot_A = CCM_boot_A, CCM_boot_B = CCM_boot_B)

# ---------------------------------------------------------------
index <- 500
Accm <- as.numeric(unlist(data$data[index,]$s))
Bccm <- as.numeric(unlist(data$data[index,]$t))

# show data
showdata(Accm, Bccm)

# determine Embedding Dimension
determineEmbeddingDimension(Accm)
E_A = 1
determineEmbeddingDimension(Bccm)
E_B = 1

# Prediction Decay
predictionDeacy(data = Accm, Em = E_A)
predictionDeacy(data = Bccm, Em = E_B)
TAU = 2
# Identifying Nonlinearity
identifyingNonlinearity(data = Accm, Em = E_A)
identifyingNonlinearity(data = Bccm, Em = E_B)

# CCM(use multispatialCCM)
signal_A_out<-SSR_check_signal(A=Accm, E=E_A, tau=TAU, predsteplist=1:10)
signal_B_out<-SSR_check_signal(A=Bccm, E=E_B, tau=TAU, predsteplist=1:10)
CCM_boot_A<-CCM_boot(Accm, Bccm, E_A, tau=TAU, iterations=30)
CCM_boot_B<-CCM_boot(Bccm, Accm, E_B, tau=TAU, iterations=30)
(CCM_significance_test<-ccmtest(CCM_boot_A, CCM_boot_B))
drawCCM(CCM_boot_A = CCM_boot_A, CCM_boot_B = CCM_boot_B)
