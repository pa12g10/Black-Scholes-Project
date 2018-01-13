import numpy as np
import pandas as pd
import time
from scipy import stats
S0 = 100
E = 100
T=1.0
r=0.05
vol=0.2
num_steps = 252
I = 10000
barrier = 120
time_start = time.clock()
dt = 1.0 /num_steps 
df = np.exp(-r*T)
rand = np.random.standard_normal((num_steps, I))
S = np.zeros_like(rand)
S_max = np.zeros((num_steps,I))
S_max[0] = S0
payoff = []
S[0] = S0
#GBM_Euler
for t in range(1,num_steps):                                
    S[t] = S[t-1] * (1 + (r * dt) + (vol * np.sqrt(dt)*rand[t]))
#Option Payoff: S(T) - E   
for j in range(0,I):          
    for p in range(1,num_steps):
        if S[p][j] > S_max[p-1][j]:
            S_max[p][j] = S[p][j] 
        elif S[p][j] <= S_max[p-1][j]:  
            S_max[p][j] = S_max[p-1][j] 
    if S_max[p][j] < barrier:
        payoff.append(0) 
    elif S[p][j] - E <= 0:  
        payoff.append(0) 
    elif S[p][j] - E > 0:    
        payoff.append((S[p][j] - E)) 
#Opt. Value:  df * [S(T) - E]      
val = df*(np.mean(payoff))
time_elapsed = (time.clock() - time_start)  
print "Option value is %f. Time to run %f. Barrier is %f." % (val,time_elapsed,barrier)