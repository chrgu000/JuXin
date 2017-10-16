# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 13:52:46 2017

@author: Administrator
"""

import matplotlib.pyplot as plt
import time,TrainModelLab,TrainModelFuture

x1=time.clock()
nameDB='test' # should be set for create a new mode test; if future should be 'futuretest'
firstTime=1
shufflePoints=0
ReGetPoints=0
TradeScan=0

dispersity=0.55
profitNot=0.2
profitOk=0.3

future='I.DCE'
minTick=0.0
longshort=-1 # 1 means long; and -1 means short
barSize=5


if nameDB[:6].lower()!='future':
    TM=TrainModelLab.TrainModel(nameDB,firstTime,shufflePoints,ReGetPoints,TradeScan,dispersity,profitNot,profitOk) #should be in turn; stocks
else:
    TM=TrainModelFuture.TrainModel(nameDB,firstTime,shufflePoints,ReGetPoints,TradeScan,dispersity,profitNot,profitOk,future,minTick,longshort,barSize) #should be in turn; futures
@TM
def ModelX(opens,highs,lows,closes):
    if closes[-2]<lows[-2]+(highs[-2]-lows[-2])/4  and closes[-1]>lows[-1]+(highs[-1]-lows[-1])*3/4  and \
            highs[-4]>lows[-4] and highs[-3]>lows[-3] and highs[-2]>lows[-2] and highs[-1]>lows[-1] and closes[-1]/closes[-2]<1.095:
        R=1
    else:
        R=0
    return R
                 
















