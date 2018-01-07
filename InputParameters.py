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
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


LARGER_FONT= ("Verdana", 14)
LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
YesNo = 0

VersionNumber = ' v1.01'

photoName = 'wallStreetBull.jpg'

DataBaseFileName = "TradeDatabase.csv"

plot_types = array(['c_delta','p_delta','gamma','gammaP','vega','c_theta',
                    'p_theta','c_rho','p_rho','c_psi','p_psi','c_carry',
                    'p_carry','DdeltaDvol','DdeltaDtime'])
BS_Model_type = array(['Espen','Norm'])
option_trade_economic_title = array(["Contract Size:","Quantity:","Strike:",
                                          "Start Date (dd-mm-yyyy):","Maturity (dd-mm-yyyy):",
                                          "Interest rate % :","Dividend Yield % :"])
option_underlyings = array(["UKX Index","SPX Index","SX5E Index","NKY Index"])
optionTradeDetailsForPlot = array(["Strike:","Maturity (Years) :","Interest rate % :","Dividend Yield % :","Sigma % :"])
option_BuySell = array(["Buy","Sell"])
option_CallPut = array(["Call","Put"])