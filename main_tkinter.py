# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:44:36 2017
@author: peallen
"""

from InputParameters import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

BS = BS(100, 100, 1,1,1,1,'Espen')

class TradeManager(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default="clienticon.ico")
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
        
        Button_TradePositions = ttk.Button(self, text="Trade Positions", command=lambda: controller.show_frame(TradePositions))
        Button_TradePositions.place(relx=.50, rely=.30) 

        Button_RiskPositions = ttk.Button(self, text="Risk Exposures" , command=lambda: controller.show_frame(RiskExposures))
        Button_RiskPositions.place(relx=.50, rely=.45)  
        
        Button_SurfacePlotter = ttk.Button(self, text="Surface Plotter" , command=lambda: controller.show_frame(SurfacePlotter))
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
        
        self.option_entry_list = [None]*len(option_trade_economic_title)
        

        underlyingList = OptionMenu(self, self.dropDownDefaultStrUnderlying, * option_underlyings )
        underlyingList.place(x =250 , y= 50 ) 
        
        BuySellList = OptionMenu(self, self.dropDownDefaultStrBuySell, * option_BuySell )
        BuySellList.place(x =250 , y= 100) 
        
        CallPutList = OptionMenu(self, self.dropDownDefaultStrCallPut, * option_CallPut )
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
            Label(self, text=option_trade_economic_title[i]).place(x =50 , y=(200 + i*50)) 
            self.option_entry_list[i] = ttk.Entry(self)
            self.option_entry_list[i].place(x =250 , y=(200 + i*50)) 
    
    def ClearTradeDetails(self):
        for i in range(0, len(self.option_entry_list)):
            self.option_entry_list[i].delete(0, 'end')
    
    def BookTrade(self):
        NewTradeID = self.getNewTradeID()
        with open(DataBaseFileName, "a") as TradeDatabase:
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
        with open(DataBaseFileName) as TradeDatabase:
           TradeID = int(list(TradeDatabase)[-1][:6]) + 1
        TradeDatabase.close()
        return TradeID
    
    def refreshPositionsList(self):
        TradeDatabase = pd.read_csv('TradeDatabase.csv', sep=';')
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
        
        self.option_stock_price_entry = [None]*len(option_underlyings)
        self.option_greek_entry = [None]*len(option_greeks)
        
        Button_BackHome = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        Button_BackHome.place(x =50 , y= 10 ) 
        
        Label(self, text="Enter Underlying Spot Prices:", font=LLARGE_FONT).place(x =400  , y=95)  
        for i in range(0, len( self.option_stock_price_entry)):
            Label(self, text=option_underlyings[i]).place(x =(700 + i*150) , y=75 ) 
            self.option_stock_price_entry[i] = ttk.Entry(self)
            self.option_stock_price_entry[i].place(x =(675 + i*150) , y=100) 
        
        Label(self, text="Portfolio Greeks Break Down", font=LLARGE_FONT).place(x =50 , y=250) 
        for i in range(0, len( self.option_greek_entry)):
            Label(self, text=option_greeks[i]).place(x =50 , y=(300 + i*75)) 
            self.option_greek_entry[i] = ttk.Entry(self)
            self.option_greek_entry[i].place(x =150 , y=(300 + i*75))    
        
                
class SurfacePlotter(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Surface Plotter", font=LLLARGE_FONT)
        label.place(relx=.50, rely=.0)  
        
        self.option_entry_list = [None]*len(optionTradeDetailsForPlot)
        
        self.dropDownDefaultStrBuySell= StringVar(self)
        self.dropDownDefaultStrPlotType = StringVar(self)
        self.dropDownDefaultStrBSModelType= StringVar(self)
        self.dropDownDefaultStrBuySell.set("Select Buy/Sell")
        self.dropDownDefaultStrPlotType.set("Select Plot Type")
        self.dropDownDefaultStrBSModelType.set("Select BS Model Type")
        
        BuySellList = OptionMenu(self, self.dropDownDefaultStrBuySell, * option_BuySell )
        BuySellList.place(x =250 , y= 100) 
        
        PlotTypeList = OptionMenu(self, self.dropDownDefaultStrPlotType, * plot_types )
        PlotTypeList.place(x =250 , y= 150) 
        
        BSModelTypeList = OptionMenu(self, self.dropDownDefaultStrBSModelType, * BS_Model_type )
        BSModelTypeList.place(x =250 , y= 200) 
        
        Button_PlotCurve = ttk.Button(self, text="Plot Curve",  command=self.plotSurface3DSurface)
        Button_PlotCurve.place(x =100 , y=600) 
        
        Button_BackHome = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        Button_BackHome.place(x =50 , y= 10 ) 
        
        for i in range(0, len( self.option_entry_list)):
            Label(self, text=optionTradeDetailsForPlot[i]).place(x =50 , y=(250 + i*50)) 
            self.option_entry_list[i] = ttk.Entry(self)
            self.option_entry_list[i].place(x =250 , y=(250 + i*50))   
            

    def plotSurface3DSurface(self):
        global BS
        BS.setParameters(100, float(self.option_entry_list[0].get()), float(self.option_entry_list[1].get()),
                 float(self.option_entry_list[2].get()),float(self.option_entry_list[3].get()),
                  float(self.option_entry_list[4].get()), self.dropDownDefaultStrBSModelType.get())
        f = BS.plot3dSurfaceTkinter(self.dropDownDefaultStrPlotType.get())
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.place(x =400 , y= 100 )       

        
app = TradeManager()
app.geometry("850x650+350+350")
app.mainloop()