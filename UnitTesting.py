# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 11:58:43 2017
UnitTesting
@author: Peter Nicholas Allen
"""
from BS_Framework import *
import unittest 
scaler = 100

O = BS(100, 100, 1.0, 0.05, 0.02,0.2,'Espen')
D = BS(90, 100, 1.0, 0.05, 0.02,0.2,'Espen')

def startUnitTest():
    unittest.main()

class MyTest(unittest.TestCase):
    def test_N(self): 
        self.assertEqual(N(0),0.5)
    def test_dN(self):
        self.assertEqual(round(dN(0), 3),0.399)
    #Pricing    
    def test_callOptPrice(self):
        self.assertEqual(round(O.callOptPrice(), 2),8.65)
    def test_putOptPrice(self):
        self.assertEqual(round(O.putOptPrice(), 2),6.73)
    def test_putCallParityCallPrice(self):
        self.assertEqual(round(O.putCallParityCallPrice(),2),8.65)
    def test_putCallParityPutPrice(self):
        self.assertEqual(round(O.putCallParityPutPrice(),2),6.73)
    #Greeks
    def test_c_delta(self):
        self.assertEqual(round(O.c_delta(),4),0.5621)
    def test_p_delta(self):
        self.assertEqual(round(O.p_delta(),4),-0.4083)
    def test_gamma(self):
        self.assertEqual(round(O.gamma(),5),0.01897)
    def test_gammaP(self):
        self.assertEqual(round(O.gammaP(),3),0.019)
    def test_vega(self):
        self.assertEqual(round(O.vega(),4),0.3795)
    def test_c_theta(self):
        self.assertEqual(round(O.c_theta(),4),-0.0123)
    def test_p_theta(self):
        self.assertEqual(round(O.p_theta(),4),-0.0072)
    def test_c_rho(self):
        self.assertEqual(round(O.c_rho(),4),0.4756)
    def test_p_rho(self):
        self.assertEqual(round(O.p_rho(),4),-0.4756)    
    def test_c_psi(self):
        self.assertEqual(round(O.c_psi(),4),-0.5621)
    def test_p_psi(self):
        self.assertEqual(round(O.p_psi(),4),0.4083)
    def test_c_carry(self):
        self.assertEqual(round(O.c_carry(),4),0.5621)
    def test_p_carry(self):
        self.assertEqual(round(O.p_carry(),4),-0.4083)
    def test_DdeltaDvol(self):
        self.assertEqual(round(D.DdeltaDvol(),6),0.9667/scaler)
    def test_DdeltaDtime(self):
        self.assertEqual(round(D.DdeltaDtime(),6),0.0336/scaler)
    #Trade Choices    
    def test_deltaNeutralStrike(self):
        self.assertEqual(round(O.deltaNeutralStrike(),4),108.3287)
    
