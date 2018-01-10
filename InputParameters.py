# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 18:56:16 2018
@author: Gebruiker
"""
from BS_Framework import *
from pandas import *	
from datetime import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from numpy import *
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


LLLARGE_FONT= ("Verdana", 14)
LLARGE_FONT= ("Verdana", 13)
LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)

now = datetime.now()

BS_Class_1 = BS(100, 100, 1,1,1,1,'Espen')

ToolBarExists = 0.0

PortfolioManagerClassOnOff = 0.0

NumDigitsRound = 3

VersionNumber = ' v1.01'

photoName = 'wallStreetBull.jpg'

DataBaseFileName = "TradeDatabase.csv"

plot_types = array(['c_delta','p_delta','gamma','gammaP','vega','c_theta',
                    'p_theta','c_rho','p_rho','c_psi','p_psi','c_carry',
                    'p_carry','DdeltaDvol','DdeltaDtime'])
BS_Model_type = array(['Espen','Norm'])
option_trade_economic_title = array(["Contract Size:","Quantity:","Strike:",
                                          "Start Date (dd-mm-yyyy):","Maturity (dd-mm-yyyy):",
                                          "Interest rate % :","Dividend Yield % :", "sigma :"])
EntryBox_Default_Option_Parameters = array([10,10,100,"10-01-2018","12-03-2018",0.05,0.02,0.2])
option_underlyings = array(["UKX Index","SPX Index","SX5E Index","NKY Index"])
option_underlyings_price = array([100,100,100,100])
#option_underlyings_price = array([7696.51,2747.39,3618.00,23714.53])
optionTradeDetailsForPlot = array(["Strike:","Maturity (Years) :","Interest rate % :","Dividend Yield % :","Sigma % :"])
optionTradeDetailsForPlot_initial_values = array([100,1,0.05,0.02,0.25])
option_BuySell = array(["Buy","Sell"])
option_CallPut = array(["Call","Put"])
option_greeks = array([ "delta","gammaP", "vegaP", "theta","rho","psi","carry","DdeltaDvol","DdeltaDtime"])