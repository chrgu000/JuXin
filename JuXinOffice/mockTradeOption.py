# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 13:19:55 2017

@author: Administrator
"""

from WindPy import *
import numpy as np

objTrade=['10000995.sh']
hands=1
openPrice=0.0190
stopLoss=0.0180
hold=0
w.start()
Tem=w.tlogon('0000', '0', 'W115294100303', '*********', 'SHO')
logId=Tem.Data[0][0]

#define the callback function
def myCallback(indata):
    global objTrade,hands,openPrice,stopLoss,hold
    if indata.ErrorCode!=0:
        print('error code:'+str(indata.ErrorCode)+'\n')
        return()
    print(indata.Data[0])
    if indata.Data[0][0]>openPrice and hold<1:
        w.torder(objTrade[0], 'Buy', indata.Data[0][0]+0.002, hands, 'OrderType=LMT;LogonID='+str(logId))
        hold=hold+1
        print('open order buy ' + objTrade[0])
    if indata.Data[0][0]<stopLoss:
        w.torder(objTrade[0], 'Sell', indata.Data[0][0]-0.002, hands, 'OrderType=LMT;LogonID='+str(logId))
        print('close order ' + objTrade[0])

data=w.wsq(','.join(objTrade),"rt_last",func=myCallback)
#w.cancelRequest(data.RequestID)
#pf.close()










