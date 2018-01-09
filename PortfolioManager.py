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
BS = BS(100, 100, 1,1,1,1,'Espen')
MatDate = '22-4-2018'
modelType = 'Espen'

TradeDatabase = pd.read_csv('TradeDatabase.csv', sep=';')
TradeDatabase = TradeDatabase.as_matrix()



def timeBetweenTwoDatesInYears(valDate, MatDate):
    Mat = datetime.strptime(MatDate, "%d-%m-%Y")
    return (((Mat - valDate).days)/yearCnt)
    
   
    
class ManagePortfolio:
    def __init__(self,TradeBlock,option_underlyings,valDate):
        self.TradeBlock =TradeBlock  
        self.option_underlyings = option_underlyings
        self.valDate = valDate
        self.FtseTrades = []
        self.SnPTrades = []
        self.EuroTrades = []
        self.NikkiTrades = []
        self.FtseTrades_greeks = []
        self.SnPTrades_greeks = []
        self.EuroTrades_greeks = []
        self.NikkiTrades_greeks = []
        self.FtseTrades_greeks.append(option_greeks)
        self.SnPTrades_greeks.append(option_greeks)
        self.EuroTrades_greeks.append(option_greeks)
        self.NikkiTrades_greeks.append(option_greeks)
        self.FtseTrades_greeks_sum = []
        self.SnPTrades_greeks_sum = []
        self.EuroTrades_greeks_sum = []
        self.NikkiTrades_greeks_sum = []
        
        
    def SeperateTradeBlockByUnderlyingAndGetTradeGreeks(self):
        for y in range(0, len(self.TradeBlock)):
            if self.TradeBlock[y][1] == self.option_underlyings[0]:
                self.FtseTrades.append(self.TradeBlock[y])                
                BS.setParameters(option_underlyings_price[0], self.TradeBlock[y][6], timeBetweenTwoDatesInYears(self.valDate,self.TradeBlock[y][8]),
                                 self.TradeBlock[y][9],self.TradeBlock[y][10], self.TradeBlock[y][11], modelType)
                self.FtseTrades_greeks.append(BS.getAllGreeksForTrade(self.TradeBlock[y]))
            elif self.TradeBlock[y][1] == self.option_underlyings[1]:
                self.SnPTrades.append(self.TradeBlock[y])                
                BS.setParameters(option_underlyings_price[1], self.TradeBlock[y][6], timeBetweenTwoDatesInYears(self.valDate,self.TradeBlock[y][8]),
                                 self.TradeBlock[y][9],self.TradeBlock[y][10], self.TradeBlock[y][11], modelType)
                self.SnPTrades_greeks.append(BS.getAllGreeksForTrade(self.TradeBlock[y]))
            elif self.TradeBlock[y][1] == self.option_underlyings[2]:
                self.EuroTrades.append(self.TradeBlock[y])                
                BS.setParameters(option_underlyings_price[2], self.TradeBlock[y][6], timeBetweenTwoDatesInYears(self.valDate,self.TradeBlock[y][8]),
                                 self.TradeBlock[y][9],self.TradeBlock[y][10], self.TradeBlock[y][11], modelType)
                self.EuroTrades_greeks.append(BS.getAllGreeksForTrade(self.TradeBlock[y]))
            elif self.TradeBlock[y][1] == self.option_underlyings[3]:
                self.NikkiTrades.append(self.TradeBlock[y])
                BS.setParameters(option_underlyings_price[3], self.TradeBlock[y][6], timeBetweenTwoDatesInYears(self.valDate,self.TradeBlock[y][8]),
                                 self.TradeBlock[y][9],self.TradeBlock[y][10], self.TradeBlock[y][11], modelType)
                self.NikkiTrades_greeks.append(BS.getAllGreeksForTrade(self.TradeBlock[y]))
        print(self.SnPTrades_greeks)
        self.setOptionGreekListsToArrays()
        
    
    def setOptionGreekListsToArrays(self):        
        self.FtseTrades_greeks = np.asarray( self.FtseTrades_greeks)
        self.SnPTrades_greeks = np.asarray( self.SnPTrades_greeks)        
        self.EuroTrades_greeks = np.asarray( self.EuroTrades_greeks)
        self.NikkiTrades_greeks = np.asarray( self.NikkiTrades_greeks)
        
#    def SumGreeksForEachUnderlying(self):
#        self.FtseTrades_greeks_sum.append(self.FtseTrades_greeks)
#        self.SnPTrades_greeks_sum.append(self.SnPTrades_greeks)
#        self.EuroTrades_greeks_sum.append(self.EuroTrades_greeks)
#        self.NikkiTrades_greeks_sum.append(self.NikkiTrades_greeks)
#        
#    def sumArrayColoumn(Array):
#        for i in range(0,len(option_greeks)):
#            sum = sum + np.sum(Array[1:len(Array)][i])

valDate = datetime.now()    
ManagePortfolio = ManagePortfolio(TradeDatabase,option_underlyings,valDate)
ManagePortfolio.SeperateTradeBlockByUnderlyingAndGetTradeGreeks()   
