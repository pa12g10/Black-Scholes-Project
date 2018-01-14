import numpy as np
from numpy import *
import matplotlib.pyplot as plt
S0 = 100.0
#K  = strike price
r = 0.05
q  = 0.0
sigma = 0.2
T = 1.0
lambda_J= 24
mu_J    = 0.1
sigma_J = 0.1
N_T = 365
dt = T/N_T
kappa = exp(mu_J) - 1.0
drift = r - q - lambda_J*kappa - 0.5*sigma*sigma
S = np.zeros(N_T)
S[0] = S0;
for t in range(1,N_T):
    J = 0
    if lambda_J == 0:
        Nt = np.random.poisson(lambda_J*dt)
        if Nt > 0:
            for i in range(1,Nt):
                J = J + np.random.normal(mu_J - (sigma_J^2)/2,sigma_J)
    Z = np.random.normal(0,1)
    S[t] = S[t-1]*exp(drift*dt + sigma*sqrt(dt)*Z + abs(J))
print(S)
plt.plot(S)
plt.ylabel('Energy Price Modelling')
plt.show()