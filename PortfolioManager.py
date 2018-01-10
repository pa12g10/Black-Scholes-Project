# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 09:18:18 2018
@author: peallen
"""

from BS_Framework import *
import numpy as np
from datetime import *
from InputParameters import *

yearCnt = 365

BS_Class_2 = BS(100, 100, 1,1,1,1,'Espen')

def timeBetweenTwoDatesInYears(valDate, MatDate):
    Mat = datetime.strptime(MatDate, "%d-%m-%Y")
    return (((Mat - valDate).days)/yearCnt)
    
class ManagePortfolio:
    def __init__(self,TradeBlock,option_underlyings,underlying_prices,valDate,modelType):
        self.TradeBlock =TradeBlock  
        self.modelType = modelType
        self.option_underlyings = option_underlyings
        self.valDate = valDate
        self.underlying_prices = underlying_prices
        self.FtseTrades = []
        self.SnPTrades = []
        self.EuroTrades = []
        self.NikkiTrades = []
        self.FtseTrades_greeks = []
        self.SnPTrades_greeks = []
        self.EuroTrades_greeks = []
        self.NikkiTrades_greeks = []
        self.FtseTrades_greeks_sum = []
        self.SnPTrades_greeks_sum = []
        self.EuroTrades_greeks_sum = []
        self.NikkiTrades_greeks_sum = []
        self.FtseTrades_posValues = []
        self.SnPTrades_posValues  = []
        self.EuroTrades_posValues  = []
        self.NikkiTrades_posValues  = []
        self.AllPortOptionMVs = []
    
    def reset(self):
        self.FtseTrades = []
        self.SnPTrades = []
        self.EuroTrades = []
        self.NikkiTrades = []
        self.FtseTrades_greeks = []
        self.SnPTrades_greeks = []
        self.EuroTrades_greeks = []
        self.NikkiTrades_greeks = []
        self.FtseTrades_greeks_sum = []
        self.SnPTrades_greeks_sum = []
        self.EuroTrades_greeks_sum = []
        self.NikkiTrades_greeks_sum = []
        self.FtseTrades_posValues = []
        self.SnPTrades_posValues  = []
        self.EuroTrades_posValues  = []
        self.NikkiTrades_posValues  = []
        self.AllPortOptionMVs = []
        
    def setParameters(self,TradeBlock,option_underlyings,underlying_prices,valDate,modelType):
        self.TradeBlock =TradeBlock  
        self.modelType = modelType
        self.option_underlyings = option_underlyings
        self.underlying_prices = underlying_prices
        self.valDate = valDate        
        self.reset()
        
    def SeperateTradeBlockByUnderlyingAndGetTradeGreeks(self):
        global BS_Class_2
        for y in range(0, len(self.TradeBlock)):
            if self.TradeBlock[y][1] == self.option_underlyings[0]:
                self.FtseTrades.append(self.TradeBlock[y])                
                BS_Class_2.setParameters(self.underlying_prices[0], self.TradeBlock[y][6], timeBetweenTwoDatesInYears(self.valDate,self.TradeBlock[y][8]),
                                 self.TradeBlock[y][9],self.TradeBlock[y][10], self.TradeBlock[y][11], self.modelType)
                self.FtseTrades_greeks.append(BS_Class_2.getAllGreeksForTrade(self.TradeBlock[y]))
                self.FtseTrades_posValues.append(BS_Class_2.getMVOptionPosition(self.TradeBlock[y]))
            elif self.TradeBlock[y][1] == self.option_underlyings[1]:
                self.SnPTrades.append(self.TradeBlock[y])                
                BS_Class_2.setParameters(self.underlying_prices[1], self.TradeBlock[y][6], timeBetweenTwoDatesInYears(self.valDate,self.TradeBlock[y][8]),
                                 self.TradeBlock[y][9],self.TradeBlock[y][10], self.TradeBlock[y][11], self.modelType)
                self.SnPTrades_greeks.append(BS_Class_2.getAllGreeksForTrade(self.TradeBlock[y]))
                self.SnPTrades_posValues.append(BS_Class_2.getMVOptionPosition(self.TradeBlock[y]))
            elif self.TradeBlock[y][1] == self.option_underlyings[2]:
                self.EuroTrades.append(self.TradeBlock[y])                
                BS_Class_2.setParameters(self.underlying_prices[2], self.TradeBlock[y][6], timeBetweenTwoDatesInYears(self.valDate,self.TradeBlock[y][8]),
                                 self.TradeBlock[y][9],self.TradeBlock[y][10], self.TradeBlock[y][11], self.modelType)
                self.EuroTrades_greeks.append(BS_Class_2.getAllGreeksForTrade(self.TradeBlock[y]))
                self.EuroTrades_posValues.append(BS_Class_2.getMVOptionPosition(self.TradeBlock[y]))
            elif self.TradeBlock[y][1] == self.option_underlyings[3]:
                self.NikkiTrades.append(self.TradeBlock[y])
                BS_Class_2.setParameters(self.underlying_prices[3], self.TradeBlock[y][6], timeBetweenTwoDatesInYears(self.valDate,self.TradeBlock[y][8]),
                                 self.TradeBlock[y][9],self.TradeBlock[y][10], self.TradeBlock[y][11], self.modelType)
                self.NikkiTrades_greeks.append(BS_Class_2.getAllGreeksForTrade(self.TradeBlock[y]))
                self.NikkiTrades_posValues.append(BS_Class_2.getMVOptionPosition(self.TradeBlock[y]))
        self.setOptionListsToArrays()
        
    
    def setOptionListsToArrays(self):        
        self.FtseTrades_greeks = np.asarray(self.FtseTrades_greeks)
        self.SnPTrades_greeks = np.asarray(self.SnPTrades_greeks)        
        self.EuroTrades_greeks = np.asarray(self.EuroTrades_greeks)
        self.NikkiTrades_greeks = np.asarray(self.NikkiTrades_greeks)
        self.FtseTrades_posValue = np.asarray(self.FtseTrades_posValues)
        self.SnPTrades_posValues = np.asarray(self.SnPTrades_posValues)        
        self.EuroTrades_posValues = np.asarray(self.EuroTrades_posValues)
        self.NikkiTrades_posValues = np.asarray(self.NikkiTrades_posValues)
        
    def SumGreeksForEachUnderlying(self):
        self.FtseTrades_greeks_sum.append(np.sum(self.FtseTrades_greeks, axis=0))
        self.SnPTrades_greeks_sum.append(np.sum(self.SnPTrades_greeks, axis=0))
        self.EuroTrades_greeks_sum.append(np.sum(self.EuroTrades_greeks, axis=0))
        self.NikkiTrades_greeks_sum.append(np.sum(self.NikkiTrades_greeks, axis=0))
        return self.joinArraysIntoOptionGreekMatrix()
    
    def SumOptionMVsForEachUnderlying(self):
        self.AllPortOptionMVs.append(np.sum(self.FtseTrades_posValue))
        self.AllPortOptionMVs.append(np.sum(self.SnPTrades_posValues))
        self.AllPortOptionMVs.append(np.sum(self.EuroTrades_posValues))
        self.AllPortOptionMVs.append(np.sum(self.NikkiTrades_posValues))
        return self.AllPortOptionMVs
        
    def joinArraysIntoOptionGreekMatrix(self):
        a = np.concatenate((self.FtseTrades_greeks_sum, self.SnPTrades_greeks_sum), axis=0)
        b = np.concatenate((self.EuroTrades_greeks_sum,self.NikkiTrades_greeks_sum), axis=0)
        return  np.concatenate((a,b), axis=0)
    