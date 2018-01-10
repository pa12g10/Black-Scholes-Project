# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:44:36 2017
@author: peallen
"""

from InputParameters import *
from PortfolioManager import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

class TradeManager(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Trade Manager"+ VersionNumber)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, TradePositions,RiskExposures,SurfacePlotter):
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
        label = tk.Label(self, text=("Equity Option Tool Manager"), font=LLLARGE_FONT)
        label.place(relx=.4, rely=.10) 
        
        image = Image.open(photoName)
        image = image.resize((350,350))
        photo = ImageTk.PhotoImage(image)
        label1 = tk.Label(self,image=photo)
        label1.image = photo # keep a reference!
        label2 = tk.Label(self,image=photo)
        label2.image = photo # keep a reference!
        label1.place(relx=.10, rely=.25)
        label2.place(relx=.70, rely=.25)
        
        Button_TradePositions = ttk.Button(self, text="Trade Positions", command=lambda: controller.show_frame(TradePositions))
        Button_RiskPositions = ttk.Button(self, text="Risk Exposures" , command=lambda: controller.show_frame(RiskExposures))
        Button_SurfacePlotter = ttk.Button(self, text="Surface Plotter" , command=lambda: controller.show_frame(SurfacePlotter))
        Button_TradePositions.place(relx=.50, rely=.30) 
        Button_RiskPositions.place(relx=.50, rely=.45)  
        Button_SurfacePlotter.place(relx=.50, rely=.60)  


class TradePositions(tk.Frame):           
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Trade Positions", font=LLLARGE_FONT)
        label.place(relx=.50, rely=.0)  
        
        self.dropDownDefaultStrUnderlying = StringVar(self)
        self.dropDownDefaultStrBuySell= StringVar(self)
        self.dropDownDefaultStrCallPut = StringVar(self)
        self.dropDownDefaultStrUnderlying.set("Select Underlying Index")
        self.dropDownDefaultStrBuySell.set("Select Buy/Sell")
        self.dropDownDefaultStrCallPut.set("Select Put/Call")
        self.EntryBox_List_Option_Economics = [None]*len(option_trade_economic_title)

        OptionMenu_underlying = OptionMenu(self, self.dropDownDefaultStrUnderlying, * option_underlyings )
        OptionMenu_BuySell = OptionMenu(self, self.dropDownDefaultStrBuySell, * option_BuySell )
        OptionMenu_CallPut = OptionMenu(self, self.dropDownDefaultStrCallPut, * option_CallPut )
        OptionMenu_underlying.place(x =250 , y= 50 ) 
        OptionMenu_BuySell.place(x =250 , y= 100) 
        OptionMenu_CallPut.place(x =250 , y= 150)
        
        Button_BackHome = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        Button_BookTrade = ttk.Button(self, text="Book Trade",  command=self.BookTrade)
        Button_ClearTrade = ttk.Button(self, text="Clear Trade Details", command=self.ClearTradeDetails)
        Button_ClearTrade = ttk.Button(self, text="Refresh Positions", command=self.refreshPositionsList)
        Button_BackHome.place(x =50 , y= 10 ) 
        Button_BookTrade.place(x =100 , y=600) 
        Button_ClearTrade.place(x =200 , y=600)
        Button_ClearTrade.place(x =500 , y=50)
        
        for i in range(0, len( self.EntryBox_List_Option_Economics)):
            Label(self, text=option_trade_economic_title[i]).place(x =50 , y=(200 + i*50)) 
            self.EntryBox_List_Option_Economics[i] = ttk.Entry(self)
            self.EntryBox_List_Option_Economics[i].place(x =250 , y=(200 + i*50)) 
            self.EntryBox_List_Option_Economics[i].insert(0, EntryBox_Default_Option_Parameters[i])
    
    def BookTrade(self):
        NewTradeID = self.getNewTradeID()
        with open(DataBaseFileName, "a") as TradeDatabase:
            TradeDatabase.write(str(NewTradeID) + ';')
            TradeDatabase.write(self.dropDownDefaultStrUnderlying.get() + ';')
            TradeDatabase.write(self.dropDownDefaultStrBuySell.get() + ';')
            TradeDatabase.write(self.dropDownDefaultStrCallPut.get() + ';')           
            for i in range(0, len(self.EntryBox_List_Option_Economics)):
                TradeDatabase.write(self.EntryBox_List_Option_Economics[i].get() + ';')
            TradeDatabase.write(str(now.strftime("%d-%m-%Y"))) 
            TradeDatabase.write('\n')             
            TradeDatabase.close()
        self.refreshPositionsList()
    
    def getNewTradeID(self):
        with open(DataBaseFileName) as TradeDatabase:
           TradeID = int(list(TradeDatabase)[-1][:6]) + 1
        TradeDatabase.close()
        return TradeID
    
    def ClearTradeDetails(self):
        for i in range(0, len(self.EntryBox_List_Option_Economics)):
            self.EntryBox_List_Option_Economics[i].delete(0, 'end')  
            
    def refreshPositionsList(self):
        TradeDatabase = pd.read_csv(DataBaseFileName, sep=';', header = 0)
        TradeDatabase = TradeDatabase.as_matrix()
        textBox = Text(self, height=25, width=125)
        scrollBar = Scrollbar(self)
        textBox.config(state=NORMAL)
        scrollBar.place(in_=textBox, relx=1.0, relheight=1.0, bordermode="inside")
        scrollBar.config(command=textBox.yview)
        textBox.config(yscrollcommand=scrollBar.set)
        textBox.delete(1.0, END)
        for y in range(0, len(TradeDatabase)):
            for x in TradeDatabase[y]:
                textBox.insert(END, x)
                textBox.insert(END,' | ')
            textBox.insert(END,'\n')
        textBox.place(x =500 , y=100)
        textBox.config(state=DISABLED)
                
class RiskExposures(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Risk Exposures", font=LLLARGE_FONT)
        label.place(relx=.50, rely=.0)  
         
        self.EntryBox_Underlying_Price = [None]*len(option_underlyings)
        self.EntryBox_Port_Pos_MVs = [None]*len(option_underlyings)
        self.underlying_prices =  [None]*len(option_underlyings)
        self.option_greek_entry = [None]*(len(option_greeks)*len(option_underlyings_price))
        
        Button_BackHome = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        Button_RefreshGreeks = ttk.Button(self, text="Refresh Greeks",command=self.RefreshGreeks)
        Button_ClearGreeks = ttk.Button(self, text="Clear Greeks",command=self.clearGreeks)
        Button_BackHome.place(x =50 , y= 10 ) 
        Button_RefreshGreeks.place(x =450 , y= 150 ) 
        Button_ClearGreeks.place(x =450, y= 200)

        ValDateLabel = Label(self, text="Valuation Date", font=LARGE_FONT).place(x =75  , y=70)  
        self.ValDateEntry = ttk.Entry(self)
        self.ValDateEntry.place(x =75  , y=95) 
        self.ValDateEntry.insert(0,now.strftime("%d-%m-%Y"))
        
        Label(self, text="Underlying Spot Prices", font=LLARGE_FONT).place(x =600  , y=80)  
        for i in range(0, len( self.EntryBox_Underlying_Price)):
            Label(self, text=option_underlyings[i]).place(x =(700 + i*150) , y=125 ) 
            self.EntryBox_Underlying_Price[i] = ttk.Entry(self)
            self.EntryBox_Underlying_Price[i].place(x =(675 + i*150) , y=150) 
            self.EntryBox_Underlying_Price[i].insert(0, option_underlyings_price[i])
        
        Label(self, text="Portfolio Greeks Break Down", font=LLARGE_FONT).place(x =600 , y=200) 
        for i in range(0, len(option_greeks)):
                Label(self, text=option_greeks[i]).place(x =600 , y=(250 + i*50)) 
        a = 0
        for j in range(0, len(option_underlyings_price)):         
            for i in range(0, len(option_greeks)):
                self.option_greek_entry[a] = ttk.Entry(self)
                self.option_greek_entry[a].place(x =(675 + 150*j) , y=(250 + i*50))         
                a += 1
        
        Label(self, text="Position Value", font=LARGE_FONT).place(x =500  , y=725)  
        for i in range(0, len( self.EntryBox_Port_Pos_MVs)):
            self.EntryBox_Port_Pos_MVs[i] = ttk.Entry(self)
            self.EntryBox_Port_Pos_MVs[i].place(x =(675 + i*150) , y=725) 
            
    def RefreshGreeks(self):
        global ManagePortfolio
        global PortfolioManagerClassOnOff
        TradeDatabase = pd.read_csv(DataBaseFileName, sep=';')
        TradeDatabase = TradeDatabase.as_matrix()
        valDate = datetime.strptime(self.ValDateEntry.get(), "%d-%m-%Y")
        underlying_prices = self.getUnderlyingPrices()
        if PortfolioManagerClassOnOff == 0.0:
            ManagePortfolio = ManagePortfolio(TradeDatabase,option_underlyings,self.underlying_prices,valDate,BS_Model_type[0])
            PortfolioManagerClassOnOff = 1.0
        ManagePortfolio.setParameters(TradeDatabase,option_underlyings,self.underlying_prices,valDate,BS_Model_type[0])
        ManagePortfolio.SeperateTradeBlockByUnderlyingAndGetTradeGreeks()
        SummaryGreekMatrix = ManagePortfolio.SumGreeksForEachUnderlying()
        PortOptionMVs = ManagePortfolio.SumOptionMVsForEachUnderlying()
        self.fillOption_greek_entry_boxes(SummaryGreekMatrix)    
        self.fillPortMVs(PortOptionMVs)
        
    def getUnderlyingPrices(self):
        for i in range(0, len( self.EntryBox_Underlying_Price)):
            self.underlying_prices[i] = float(self.EntryBox_Underlying_Price[i].get())
    
    def clearGreeks(self):
        a = 0
        for j in range(0, len(option_underlyings_price)):         
            for i in range(0, len(option_greeks)):
                self.option_greek_entry[a].delete(0, 'end')        
                a += 1
        for j in range(0,len(self.EntryBox_Port_Pos_MVs)):
            self.EntryBox_Port_Pos_MVs[j].delete(0, 'end')
    
    def fillOption_greek_entry_boxes(self, GreekMatrix):
        a = 0
        for j in range(0, len(option_underlyings_price)):         
            for i in range(0, len(option_greeks)):
                self.option_greek_entry[a].delete(0, 'end')
                self.option_greek_entry[a].insert(0,round(GreekMatrix[j][i],NumDigitsRound)) 
                a += 1
                
    def fillPortMVs(self, PortOptionMVs):
        for i in range(0, len(PortOptionMVs)):
                self.EntryBox_Port_Pos_MVs[i].delete(0, 'end')
                self.EntryBox_Port_Pos_MVs[i].insert(0,round(PortOptionMVs[i],NumDigitsRound)) 
                
class SurfacePlotter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Surface Plotter", font=LLLARGE_FONT)
        label.place(relx=.50, rely=.0)  
        
        self.EntryBox_List_Option_Economics = [None]*len(optionTradeDetailsForPlot)
        self.dropDownDefaultStrPlotType = StringVar(self)
        self.dropDownDefaultStrBSModelType= StringVar(self)
        self.dropDownDefaultStrPlotType.set("Select Plot Type")
        self.dropDownDefaultStrBSModelType.set("Select BS Model Type")
        
        OptionMenu_PlotType = OptionMenu(self, self.dropDownDefaultStrPlotType, * plot_types )
        OptionMenu_BSModelType = OptionMenu(self, self.dropDownDefaultStrBSModelType, * BS_Model_type ) 
        OptionMenu_PlotType.place(x =250 , y= 150) 
        OptionMenu_BSModelType.place(x =250 , y= 200)
        
        Button_PlotCurve = ttk.Button(self, text="Refresh Curve",  command=self.plotSurface3DSurface)
        Button_BackHome = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage)) 
        Button_PlotCurve.place(x =100 , y=600) 
        Button_BackHome.place(x =50 , y= 10 )        
        
        for i in range(0, len( self.EntryBox_List_Option_Economics)):
            Label(self, text=optionTradeDetailsForPlot[i]).place(x =50 , y=(250 + i*50)) 
            self.EntryBox_List_Option_Economics[i] = ttk.Entry(self)
            self.EntryBox_List_Option_Economics[i].place(x =250 , y=(250 + i*50)) 
            self.EntryBox_List_Option_Economics[i].insert(0,optionTradeDetailsForPlot_initial_values[i])
            
    def plotSurface3DSurface(self):
        global BS_Class_1
        global ToolBarExists
        BS_Class_1.setParameters(100, float(self.EntryBox_List_Option_Economics[0].get()), float(self.EntryBox_List_Option_Economics[1].get()),
                 float(self.EntryBox_List_Option_Economics[2].get()),float(self.EntryBox_List_Option_Economics[3].get()),
                  float(self.EntryBox_List_Option_Economics[4].get()), self.dropDownDefaultStrBSModelType.get())
        f = plt.figure()
        f.set_size_inches(14, 9)
        canvas = FigureCanvasTkAgg(f, self)
        canvas._tkcanvas.place(x =400 , y= 100 ) 
        f = BS_Class_1.plot3dSurfaceTkinter(self.dropDownDefaultStrPlotType.get(), f)
        canvas.get_tk_widget().place(x =400 , y= 100 )
        canvas.show()
        if ToolBarExists == 0.0:
            toolbar = NavigationToolbar2TkAgg(canvas, self)
            ToolBarExists = 1.0
        toolbar.update()
              
app = TradeManager()
app.geometry("850x650+350+350")
app.mainloop()