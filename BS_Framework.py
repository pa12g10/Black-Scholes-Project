# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 18:23:54 2017

@author: Peter Nicholas Allen 
"""

from math import *
from numpy import *
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
   
    
class BS:
    def __init__(self, stokePrice, strike, timeMat, intRate, divYield, sigma):
        self.stokePrice = stokePrice
        self.strike  = strike  
        self.timeMat = timeMat
        self.intRate = intRate
        self.divYield = divYield
        self.sigma = sigma
        self.dayCount = 365.0
        self.newLine = "\n"
        self.sep = "---------------"
        
   
    def fullSummary(self):
        self.pricingSummary()
        self.greekSummary()
    
    
    
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

    
    def get3DplotOptPrice(self):
        stokePrice_array = []
        timeMat_array = []
        optPrce_array = []
        
        
    

    
    def callOptPrice(self):
        return exp(- self.divYield) * self.stokePrice * N(self.d1()) - exp(- self.intRate) * self.strike * N(self.d2())
    
    def putOptPrice(self):   
        return exp(- self.intRate) * self.strike * N(- self.d2()) - exp(- self.divYield) * self.stokePrice * N(- self.d1())
    
    def putCallParityPutPrice(self):
        return self.callOptPrice() - exp(-self.divYield)*self.stokePrice + exp(-self.intRate)*self.stokePrice
    
    def putCallParityCallPrice(self):
        return self.putOptPrice() + exp(-self.divYield)*self.stokePrice - exp(-self.intRate)*self.stokePrice
    
    def c_delta(self):
        return exp(- self.divYield) * N(self.d1())
    
    def p_delta(self):
        return exp(- self.divYield) * ( 1.0 - N(self.d1()))
    
    def gamma(self):
        top = exp(- self.divYield) * dN(self.d1())
        bott = self.sigma * self.stokePrice * sqrt(self.timeMat)
        return top / bott   
    
    def vega(self):
        return self.stokePrice * sqrt(self.timeMat) * exp(- self.divYield * self.timeMat) * dN(self.d1()) / 100
    
    def c_theta(self):
        top = - self.sigma * self.stokePrice * exp(- self.divYield * self.timeMat) * dN(self.d1())
        bott = 2.0 * sqrt(self.timeMat)
        term1 = top / bott
        term2 = self.divYield * self.stokePrice * exp(- self.divYield * self.timeMat) * N(self.d1())
        term3 = - self.intRate * self.strike * exp(-self.intRate * self.timeMat) * N(self.d2())
        return (term1 + term2 + term3) / self.dayCount
    
    def p_theta(self):
        top = - self.sigma * self.stokePrice * exp(- self.divYield * self.timeMat) * dN(self.d1())
        bott = 2.0 * sqrt(self.timeMat)
        term1 = top / bott
        term2 = - self.divYield * self.stokePrice * exp(- self.divYield * self.timeMat) * N(self.d1())
        term3 = self.intRate * self.strike * exp(-self.intRate * self.timeMat) * N(self.d2())
        return term1 + term2 + term3
    
    def rho(self):
        return self.timeMat * self.strike * exp(- self.intRate * self.timeMat) * N(self.d2())
    
    def psi(self):
        return - self.timeMat * self.stokePrice * exp(- self.divYield * self.timeMat) * N(self.d1())
    
    def d1(self):
        top = log(self.stokePrice / self.strike) + (self.intRate - self.divYield + 0.5*self.sigma*self.sigma)*self.timeMat
        bott = self.sigma * sqrt(self.timeMat)
        return top/ bott
    
    def d2(self):
        return self.d1() - self.sigma * sqrt(self.timeMat)    

   
def N(X):
        return norm.cdf(X)   
    
def dN(X):
        return (1/sqrt(2*pi)) * exp(- 0.5 * X * X)