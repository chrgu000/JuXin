# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:13:42 2017

@author: Administrator
"""
#import tkinter as tk  
#window = tk.Tk()  
#window.title('my window')  
#window.geometry('200x200')  
#  
#var = tk.StringVar()  
#l = tk.Label(window,bg='yellow',width=20,text='empty')  
#l.pack()  
#  
#def print_selection():  
#    l.config(text='you have selected'+var.get())  # lable中的参数都是可以改的    
#r1 = tk.Radiobutton(window,text='Option A',variable=var,value='A',  
#                    command=print_selection)  
#r1.pack()  
#r2 = tk.Radiobutton(window,text='Option B',variable=var,value='B',  
#                    command=print_selection)  
#r2.pack()  
#  
#r3 = tk.Radiobutton(window,text='Option C',variable=var,value='C',  
#                    command=print_selection)  
#r3.pack()  
#window.mainloop()  



from WindPy import *
from termcolor import *
import numpy as np
import tkinter as tk  
import time,datetime,pdb,pickle

objTrade=['10001019.SH','J1801.DCE']
priceTarget=[0.0075,-1666.0] # P>0 means warning appears when price is more than set price; P<0 means warning appears when price is less than set price

w.start()
#define the callback function
def myCallback(indata):
    print('-'*50)
    print(time.strftime('%H:%M:%S'))
    Codes=indata.Codes
    textAdd=[]
    diffP=[]
    for i in range(len(Codes)):
        obji=objTrade.index(Codes[i])
        if priceTarget[obji]>0 and indata.Data[0][i]>priceTarget[obji]:
            tem=str(Codes[i])+' is more than set-price!'
            cprint(tem,'red')
            textAdd.append(tem)
        elif priceTarget[obji]<0 and indata.Data[0][i]<-priceTarget[obji]:
            tem=str(Codes[i])+' is less than set-price!'
            cprint(tem,'red')
            textAdd.append(tem)
        else:
            if priceTarget[obji]>0:
                diffP.append(Codes[i]+' diff:'+str(priceTarget[obji]-indata.Data[0][i]))
            else:
                diffP.append(Codes[i]+' diff:'+str(indata.Data[0][i]+priceTarget[obji]))
    if len(textAdd):
        window = tk.Tk()  
        window.title('Warning')  
        window.geometry('300x200')  
#        var = tk.StringVar()  
        l = tk.Label(window,bg='yellow',width=50,text='\n'.join(textAdd))  
        l.pack()  
        window.mainloop()    
    if len(diffP):
        print('\n'.join(diffP))
        
    
data=w.wsq(','.join(objTrade),"rt_last",func=myCallback)

'''
w.cancelRequest(data.RequestID)
'''