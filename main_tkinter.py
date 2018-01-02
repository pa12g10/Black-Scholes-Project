# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:44:36 2017

@author: peallen
"""

from pandas import *	
from datetime import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from pandas import *
from numpy import *
import matplotlib as plt
import pandas as pd

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
YesNo = 0

def tradeConfirmation(msg):
    def NO_func():
        global YesNo
        popup.destroy()
        YesNo = 0
        
    def YES_func():
        global YesNo
        popup.destroy()
        YesNo = 1
     
    popup = tk.Tk()
    popup.wm_title("Message")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x",pady=10)
    B1 = ttk.Button(popup, text = "Yes", command =  YES_func)
    B2 = ttk.Button(popup, text = "No", command =  NO_func)
    B1.pack()    
    B2.pack()
    popup.mainloop()
    return YesNo

class TradeManager(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Trade Manager")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, TradePositions,RiskExposures):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("Equity Option Tool Manager"), font=LARGE_FONT)
        label.place(relx=.4, rely=.10) 

        Button_TradePositions = ttk.Button(self, text="Trade Positions", command=lambda: controller.show_frame(TradePositions))
        Button_TradePositions.place(relx=.50, rely=.30) 

        Button_RiskPositions = ttk.Button(self, text="Risk Exposures" , command=lambda: controller.show_frame(RiskExposures))
        Button_RiskPositions.place(relx=.50, rely=.45)  


class TradePositions(tk.Frame):
            
    def __init__(self, parent, controller):
        self.DataBaseFileName = "TradeDatabase.csv"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Trade Positions", font=LARGE_FONT)
        label.place(relx=.50, rely=.0)  
        
        self.dropDownDefaultStrUnderlying = StringVar(self)
        self.dropDownDefaultStrBuySell= StringVar(self)
        self.dropDownDefaultStrCallPut = StringVar(self)
        self.dropDownDefaultStrUnderlying.set("Select Underlying Index")
        self.dropDownDefaultStrBuySell.set("Select Buy/Sell")
        self.dropDownDefaultStrCallPut.set("Select Put/Call")
        
        self.option_trade_economic_title = array(["Contract Size:","Quantity:","Strike:","Start Date (dd-mm-yyyy):","Maturity (dd-mm-yyyy):","Interest rate:","Dividend Yield"])
        self.option_entry_list = [None]*len(self.option_trade_economic_title)
        self.option_underlyings = array(["UKX Index","SPX Index","SX5E Index","NKY Index"])
        self.option_BuySell = array(["Buy","Sell"])
        self.option_CallPut = array(["Call","Put"])
        

        underlyingList = OptionMenu(self, self.dropDownDefaultStrUnderlying, * self.option_underlyings )
        underlyingList.place(x =250 , y= 50 ) 
        
        BuySellList = OptionMenu(self, self.dropDownDefaultStrBuySell, * self.option_BuySell )
        BuySellList.place(x =250 , y= 100) 
        
        CallPutList = OptionMenu(self, self.dropDownDefaultStrCallPut, * self.option_CallPut )
        CallPutList.place(x =250 , y= 150) 
        
        Button_BackHome = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        Button_BackHome.place(x =50 , y= 10 ) 
        
        Button_BookTrade = ttk.Button(self, text="Book Trade",  command=self.BookTrade)
        Button_BookTrade.place(x =100 , y=600) 
        
        Button_ClearTrade = ttk.Button(self, text="Clear Trade Details", command=self.ClearTradeDetails)
        Button_ClearTrade.place(x =200 , y=600)
        
        Button_ClearTrade = ttk.Button(self, text="Refresh Positions", command=self.refreshPositionsList)
        Button_ClearTrade.place(x =500 , y=50)
        
        
        for i in range(0, len( self.option_entry_list)):
            Label(self, text=self.option_trade_economic_title[i]).place(x =50 , y=(200 + i*50)) 
            self.option_entry_list[i] = ttk.Entry(self)
            self.option_entry_list[i].place(x =250 , y=(200 + i*50)) 
    
    def ClearTradeDetails(self):
        for i in range(0, len(self.option_entry_list)):
            self.option_entry_list[i].delete(0, 'end')
    
    def BookTrade(self):
        NewTradeID = self.getNewTradeID()
        with open(self.DataBaseFileName, "a") as TradeDatabase:
            TradeDatabase.write(str(NewTradeID) + ';')
            TradeDatabase.write(self.dropDownDefaultStrUnderlying.get() + ';')
            TradeDatabase.write(self.dropDownDefaultStrBuySell.get() + ';')
            TradeDatabase.write(self.dropDownDefaultStrCallPut.get() + ';')           
            for i in range(0, len(self.option_entry_list)):
                TradeDatabase.write(self.option_entry_list[i].get() + ';')
            TradeDatabase.write(str(datetime.now())) 
            TradeDatabase.write('\n')             
            TradeDatabase.close()
    
    def getNewTradeID(self):
        with open(self.DataBaseFileName) as TradeDatabase:
           TradeID = int(list(TradeDatabase)[-1][:6]) + 1
        TradeDatabase.close()
        return TradeID
    
    def refreshPositionsList(self):
        TradeDatabase = pd.read_csv('TradeDatabase.csv', sep=';')
        TradeDatabase = TradeDatabase.as_matrix()
        t = Text(self, height=25, width=125)
        s = Scrollbar(self)
        t.config(state=NORMAL)
        s.place(in_=t, relx=1.0, relheight=1.0, bordermode="inside")
        s.config(command=t.yview)
        t.config(yscrollcommand=s.set)
        t.delete(1.0, END)
        for y in range(0, len(TradeDatabase)):
            for x in TradeDatabase[y]:
                t.insert(END, x)
                t.insert(END,' | ')
            t.insert(END,'\n')
        t.place(x =500 , y=100)
        t.config(state=DISABLED)
                
    
            
class RiskExposures(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Risk Exposures", font=LARGE_FONT)
        label.grid(row=0, column=10)

        Button_BackHome = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        Button_BackHome.grid(row=8, column=3)

app = TradeManager()
app.geometry("850x650+350+350")
app.mainloop()