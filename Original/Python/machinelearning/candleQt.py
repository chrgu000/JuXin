# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 16:32:38 2017

@author: Administrator
"""
import sys
from PyQt5 import QtWidgets 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import matplotlib.finance as mpf
 
class Window(QtWidgets.QDialog):
    def __init__(self,Data,parent=None):
        super().__init__(parent) 
        self.candleData=Data[0]
        self.plots=len(Data)
        if self.plots>1:
            self.lineData=Data[1]
            
        self.figure = plt.figure(figsize=(30,18))
        self.axes = self.figure.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(True)
        self.canvas = FigureCanvas(self.figure)
  
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
 
        # Just some button 
#        self.button1 = QtWidgets.QPushButton('Plot')
#        self.button1.clicked.connect(self.plot)
 
        self.button2 = QtWidgets.QPushButton('Zoom')
        self.button2.clicked.connect(self.zoom)
         
        self.button3 = QtWidgets.QPushButton('Pan')
        self.button3.clicked.connect(self.pan)
         
        self.button4 = QtWidgets.QPushButton('Home')
        self.button4.clicked.connect(self.home)
 
 
        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        btnlayout = QtWidgets.QHBoxLayout()
#        btnlayout.addWidget(self.button1)
        btnlayout.addWidget(self.button2)
        btnlayout.addWidget(self.button3)
        btnlayout.addWidget(self.button4)
        qw = QtWidgets.QWidget(self)
        qw.setLayout(btnlayout)
        layout.addWidget(qw)        
        self.setLayout(layout)
        
    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()         
    def plot(self):
#        candleData=[[1,10.0,11.0,10.0,10.5],[2,10.2,11.3,9.6,10.5],[3,11.0,11.0,10.0,10.5],[4,12.2,13.3,11.6,13.1]]
        [obj.insert(0,i) for i,obj in enumerate(self.candleData)]
        mpf.candlestick_ohlc(self.axes,self.candleData,width=0.8,colorup='r',colordown='g')
        self.axes.grid()
        print(self.plots)
        if self.plots>1:
            for i in range(len(self.lineData)):
                self.axes.plot(self.lineData[i][0],self.lineData[i][1],color=self.lineData[i][2])
        self.canvas.draw()

def candle(Data):
    app = QtWidgets.QApplication(sys.argv) 
    main = Window(Data)
    main.setWindowTitle('Simple QTpy and MatplotLib example with Zoom/Pan')
    main.show() 
    main.plot()
    sys.exit(app.exec_())
        

   
    
 
        
        
        
        