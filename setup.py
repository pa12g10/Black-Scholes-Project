# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 18:27:21 2018

@author: Gebruiker
"""

from cx_Freeze import setup, Executable

setup(name = "Equity Vol Tool" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("InputParameters.py","main_tkinter","PortfolioManager","BS_Framework")])