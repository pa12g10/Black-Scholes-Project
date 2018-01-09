# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 18:23:54 2017
@author: Peter Nicholas Allen 
"""
from math import *
from numpy import *
from scipy.stats import norm
from IPython import get_ipython
import numpy as np
from matplotlib import cm 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

class BS:
    def __init__(self, stokePrice, strike, timeMat, intRate, divYield, sigma, modelType):
        self.stokePrice = stokePrice
        self.strike  = strike  
        self.timeMat = timeMat
        self.intRate = intRate
        self.divYield = divYield
        self.sigma = sigma
        self.newLine = "\n"
        self.sep = "---------------"
        self.dayCount = 365.0
        self.rateScaler = 100.0
        self.bpScaler = 10000.0
        self.modelType = modelType
    
    def setParameters(self, stokePrice, strike, timeMat, intRate, divYield, sigma, modelType):
        self.stokePrice = stokePrice
        self.strike  = strike  
        self.timeMat = timeMat
        self.intRate = intRate
        self.divYield = divYield
        self.sigma = sigma
        self.modelType = modelType
                    
    #Full summary
    def summary(self):
        self.pricingSummary()
        self.greekSummary()
        self.tradeSummary()
     
    #Pricing Summary 
    def pricingSummary(self):
        out = "Option Pricing Summary"+ self.newLine
        out = out + self.sep + self.newLine + "Input Parameters" + self.newLine + self.sep + self.newLine
        out = out + "Stoke Price: {}".format(self.stokePrice) + self.newLine
        out = out + "Strike: {}".format(self.strike) + self.newLine
        out = out + "Time to Maturity: {}".format(self.timeMat) + self.newLine
        out = out + "Interest Rate: {}".format(self.intRate) + self.newLine 
        out = out + "Dividend yield: {}".format(self.divYield) + self.newLine
        out = out + "Sigma: {}".format(self.sigma) + self.newLine 
        out = out + self.sep + self.newLine
        out = out + "Call option price: {}".format(self.callOptPrice()) + self.newLine
        out = out + "Put option price: {}".format(self.putOptPrice()) + self.newLine
        out = out + "-------END--------" + self.newLine
        print(out)
    
        #Greeks Summary 
    def greekSummary(self):
        out = "Option Greeks Summary"+ self.newLine
        out = out + self.sep + self.newLine 
        out = out + "c_delta: {}".format(self.c_delta()) + self.newLine
        out = out + "p_delta: {}".format(self.p_delta()) + self.newLine
        out = out + "gamma: {}".format(self.gamma()) + self.newLine
        out = out + "vega: {}".format(self.vega()) + self.newLine 
        out = out + "c_theta: {}".format(self.c_theta()) + self.newLine
        out = out + "p_theta: {}".format(self.p_theta()) + self.newLine 
        out = out + "-------END-------"+ self.newLine 
        print(out)
        
    #Greeks Summary 
    def tradeSummary(self):
        out = "Trade Summary"+ self.newLine
        out = out + self.sep + self.newLine 
        out = out + "Delta neutral strike is: {}".format(self.deltaNeutralStrike()) + self.newLine
        out = out + "-------END-------"+ self.newLine 
        print(out)    
        
    #Pricing 
    def d1(self):
        if self.modelType == 'Espen':
            top = log(self.stokePrice / self.strike) + (self.divYield + 0.5*self.sigma*self.sigma)*self.timeMat
        elif self.modelType == 'Norm':
            top = log(self.stokePrice / self.strike) + (self.intRate - self.divYield + 0.5*self.sigma*self.sigma)*self.timeMat
        bott = self.sigma * sqrt(self.timeMat)
        return top/ bott
    
    def d2(self):
        return self.d1() - self.sigma * sqrt(self.timeMat)
    
    def callOptPrice(self):
        return exp((self.divYield - self.intRate)*self.timeMat) * self.stokePrice * N(self.d1()) - exp(- self.intRate*self.timeMat) * self.strike * N(self.d2())
    
    def putOptPrice(self):   
        return exp(- self.intRate*self.timeMat) * self.strike * N(- self.d2()) - exp((self.divYield - self.intRate)*self.timeMat) * self.stokePrice * N(- self.d1())
    
    def putCallParityPutPrice(self):
        return self.callOptPrice() - exp((self.divYield -   self.intRate)*self.timeMat)*self.stokePrice + exp(-self.intRate*self.timeMat)*self.strike
    
    def putCallParityCallPrice(self):
        return self.putOptPrice() + exp((self.divYield - self.intRate)*self.timeMat)*self.stokePrice - exp(-self.intRate*self.timeMat)*self.strike
    
    #Greeks
    def c_delta(self):
        return exp((self.divYield - self.intRate)*self.timeMat) * N(self.d1())
    
    def p_delta(self):
        return - exp((self.divYield - self.intRate)*self.timeMat) * (N(-self.d1()))
    
    def gamma(self):
        top = exp((self.divYield - self.intRate)*self.timeMat)*dN(self.d1())
        bott = self.sigma*self.stokePrice*sqrt(self.timeMat)
        return top / bott
    
    def gammaP(self):
        return (100 * self.gamma()) / self.stokePrice
    
    def vega(self):
        return self.stokePrice*sqrt(self.timeMat)*exp((self.divYield - self.intRate)*self.timeMat)*dN(self.d1()) / 100
    
    def vegaP(self):
        return self.sigma / 10 * self.vega()
    
    def c_theta(self):
        top = - self.sigma*self.stokePrice*exp((self.divYield - self.intRate)*self.timeMat) * dN(self.d1())
        bott = 2.0 * sqrt(self.timeMat)
        term1 = top / bott
        term2 = - (self.divYield - self.intRate) * self.stokePrice * exp((self.divYield - self.intRate) * self.timeMat) * N(self.d1())
        term3 = - self.intRate * self.strike * exp(-self.intRate * self.timeMat) * N(self.d2())
        return (term1 + term2 + term3) /  self.dayCount
    
    def p_theta(self):
        top = - self.sigma * self.stokePrice * exp((self.divYield - self.intRate) * self.timeMat) * dN(self.d1())
        bott = 2.0 * sqrt(self.timeMat)
        term1 = top / bott
        term2 = (self.divYield - self.intRate) * self.stokePrice * exp((self.divYield - self.intRate) * self.timeMat) * N(-self.d1())
        term3 =  self.intRate * self.strike * exp(-self.intRate * self.timeMat) * N(-self.d2())
        return (term1 + term2 + term3) /  self.dayCount
    
    def c_rho(self):
        return self.timeMat * self.strike * exp(- self.intRate * self.timeMat) * N(self.d2()) / self.rateScaler
    
    def p_rho(self):
        return -self.timeMat * self.strike * exp(- self.intRate * self.timeMat) * N(-self.d2()) / self.rateScaler
    
    def c_psi(self):
        return -self.timeMat * self.stokePrice * exp((self.divYield - self.intRate) * self.timeMat) * N(self.d1()) / self.rateScaler
    
    def p_psi(self):
        return self.timeMat * self.stokePrice * exp((self.divYield - self.intRate) * self.timeMat) * N(-self.d1()) / self.rateScaler 
    
    def c_carry(self):
        return self.timeMat * self.stokePrice * exp((self.divYield - self.intRate) * self.timeMat) * N(self.d1()) / self.rateScaler
    
    def p_carry(self):
        return -self.timeMat * self.stokePrice * exp((self.divYield - self.intRate) * self.timeMat) * N(-self.d1()) / self.rateScaler 

    def DdeltaDvol(self):
        return (- exp((self.divYield - self.intRate)*self.timeMat)*dN(self.d1())*self.d2() / self.sigma) / self.rateScaler
    
    def DdeltaDtime(self):
        a = self.divYield / (self.sigma*sqrt(self.timeMat))
        b = self.d2() / (2.0 *self.timeMat)
        term2 = dN(self.d1())*(a - b)
        term3 = (self.divYield - self.intRate)*N(self.d1())
        return (exp((self.divYield - self.intRate)*self.timeMat) * (term2 + term3)) / self.dayCount
    
    #Trade Choices
    def deltaNeutralStrike(self):
        return ((self.stokePrice*self.stokePrice) / self.strike) * exp(2.0 * (self.divYield + 0.5 * self.sigma * self.sigma)*self.timeMat)
    
    def plot3dSurface(self, plotType, PlotInOutConsole):
        if PlotInOutConsole == 'IN':
            get_ipython().run_line_magic('matplotlib', 'inline')
        elif PlotInOutConsole == 'OUT':
            get_ipython().run_line_magic('matplotlib', 'qt')
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        X = np.arange(0, self.strike*2, 5)
        Y = np.arange(0, self.timeMat*2.0, 0.05)
        X, Y = np.meshgrid(X, Y)
        Op = BS( X , self.strike, Y, self.intRate, self.divYield , self.sigma, self.modelType)
        Z = self.callPlotType(plotType, Op)
        surface = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=0, antialiased=False)    
        fig.colorbar(surface, shrink=0.5, aspect=5)
        plt.show()
        
    def plot3dSurfaceTkinter(self,plotType,f):
        sub = f.add_subplot(1,1,1, projection = "3d")
        X = np.arange(0,  self.strike*2, 5)
        Y = np.arange(0,  self.timeMat, 0.05)
        X,Y = np.meshgrid(X,Y)
        self.setParameters( X ,  self.strike, Y,  self.intRate,  self.divYield ,  self.sigma,  self.modelType)
        Z = self.callPlotType(plotType, self)
        sub.clear()
        sub.plot_surface(X,Y,Z)
        sub.set_xlabel('Stock Price', fontsize=15)
        sub.set_ylabel('Time Maturity (Years)', fontsize=15)
        sub.set_zlabel(plotType, fontsize=15)
        return f
    
    def callPlotType(self, plotType, BS):
        if plotType == 'c_delta':
            Z = BS.c_delta()
        elif plotType == 'p_delta':
            Z =  BS.p_delta()
        elif plotType == 'gamma':
            Z =  BS.gamma()
        elif plotType == 'gammaP':
            Z =  BS.gammaP()
        elif plotType == 'vega':
            Z =  BS.vega()
        elif plotType == 'vegaP':
            Z =  BS.vegaP()
        elif plotType == 'c_theta':
            Z =  BS.c_theta()
        elif plotType == 'p_theta':
            Z =  BS.p_theta()
        elif plotType == 'c_rho':
            Z =  BS.c_rho()  
        elif plotType == 'p_rho':
            Z =  BS.p_rho()   
        elif plotType == 'c_psi':
             Z =  BS.c_psi()
        elif plotType == 'p_psi':
             Z =  BS.p_psi()
        elif plotType == 'c_carry':
             Z =  BS.c_carry()
        elif plotType == 'p_carry':
             Z =  BS.p_carry()
        elif plotType =='DdeltaDvol':
            Z = BS.DdeltaDvol()
        elif plotType == 'DdeltaDtime':
            Z = BS.DdeltaDtime()
        return Z      
        
    
    def getAllGreeksForTrade(self,TradeDetailsMatrix):
        option_Greeks = []
        if TradeDetailsMatrix[3] == 'Call':
            option_Greeks.append(self.c_delta())
            option_Greeks.append(self.gammaP())
            option_Greeks.append(self.vegaP())
            option_Greeks.append(self.c_theta())
            option_Greeks.append(self.c_rho())
            option_Greeks.append(self.c_psi())
            option_Greeks.append(self.c_carry())
            option_Greeks.append(self.DdeltaDvol())
            option_Greeks.append(self.DdeltaDtime())   
        elif TradeDetailsMatrix[3] == 'Put':
            option_Greeks.append(self.p_delta())
            option_Greeks.append(self.gammaP())
            option_Greeks.append(self.vegaP())
            option_Greeks.append(self.p_theta())
            option_Greeks.append(self.p_rho())
            option_Greeks.append(self.p_psi())
            option_Greeks.append(self.p_carry())
            option_Greeks.append(self.DdeltaDvol())
            option_Greeks.append(self.DdeltaDtime())
        option_Greeks = asarray(option_Greeks)
        option_Greeks = self.scaleUpGreekByOptionQunantityAndSize(option_Greeks,TradeDetailsMatrix[4],TradeDetailsMatrix[5])
        if TradeDetailsMatrix[2] == 'Sell':
            option_Greeks = -1*option_Greeks
        return option_Greeks
        
    def scaleUpGreekByOptionQunantityAndSize(self,option_Greeks,ContractSize,Quanity):
        return option_Greeks*ContractSize*Quanity
  
def N(X):
        return norm.cdf(X)   
    
def n(X):
        return norm.ppf(X)
    
def dN(X):
        return (1/sqrt(2*pi)) * exp(- 0.5 * X * X)