# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 00:08:38 2017

@author: Gebruiker
"""

import tkinter as tk
from tkinter import ttk
import matplotlib 
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure 
import matplotlib.animation as animation 
from matplotlib import style

LARGE_FONT = ("Verdana",12)
style.use("ggplot")


#def anima():
#    pulldata


class TradeManager(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        
        tk.Tk.iconbitmap(self, default = "ClientIcon2.ico")
        tk.Tk.wm_title(self, "Trade Manager")
        
        container = tk.Frame(self)
        container.pack(side="top", fill = "both",expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)        
        
        self.frames = {}
        
        for F in (startPage, PageOne, PageTwo, PageThree):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column = 0, sticky = "nsew")
        self.show_frame(startPage)
    
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

def qf(stringtoprint):
    print(stringtoprint)
        
class startPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 10, padx=10)
        
        button1 = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()
        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        button2 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button2.pack()
        
class PageOne(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text = "Page One", font = LARGE_FONT)
        label.pack(pady = 10, padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(startPage))
        button1.pack()
        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        
        
class PageTwo(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text = "Page Two", font = LARGE_FONT)
        label.pack(pady = 10, padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(startPage))
        button1.pack()
        button2 = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        
class PageThree(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text = "Graph Page", font = LARGE_FONT)
        label.pack(pady = 10, padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(startPage))
        button1.pack()
        
        f = Figure(figsize = (5,5), dpi = 100)
        a = f.add_subplot(111)
        a.plot((1,2,3,4,5,6,7,8),(5,6,7,8,9,11,15,17))
        canvas = FigureCanvasTkAgg(f,self)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        toolbar = NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        
app = TradeManager()
app.mainloop()
        