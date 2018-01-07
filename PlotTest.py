# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:44:29 2018

@author: Gebruiker
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from BS_Framework import *
get_ipython().run_line_magic('matplotlib', 'qt')
plotType = 'c_delta'
strike = 100
timeMat = 1
intRate = 0.05
divYield = 0
sigma = 0.2
modelType = 'Espen'
fig = plt.figure()
sub = fig.add_subplot(1,1,1, projection = "3d")
X = np.arange(0, strike*2, 5)
Y = np.arange(0, timeMat*2.0, 0.05)
X,Y = np.meshgrid(X,Y)
Op = BS( X , strike, Y, intRate, divYield , sigma, modelType)
Z = Op.callPlotType(plotType, Op)
sub.plot_surface(X,Y,Z)
fig.show()