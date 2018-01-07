# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 23:30:53 2018

@author: Gebruiker
"""

from BS_Framework import *

BS = BS(100, 100, 1, 0.05, 0.0, 0.2, 'Espen')
BS.plot3dSurface('c_delta','OUT')
f = BS.plot3dSurfaceTkinter(100,365,0.05,0.0,0.2,'Espen','c_delta')