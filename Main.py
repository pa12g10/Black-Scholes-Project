# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 20:37:54 2017

@author: Peter Allen 
@background: This script is used to run the different pricing and greeks figures from BS_Framework.py

"""

from BS_Framework import *
import matplotlib as plt
#Initilise Class
O = BS(100, 100, 1.0, 0.0, 0.00,0.20)

#Full Option Summary
O.fullSummary()
