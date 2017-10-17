# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 13:52:46 2017

@author: Administrator
"""

import matplotlib.pyplot as plt
import time,TrainModel,TrainModelFuture

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
    TM=TrainModel.TrainModel(nameDB,firstTime,shufflePoints,ReGetPoints,TradeScan,dispersity,profitNot,profitOk) #should be in turn; stocks
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
                 
flagNot,flagOk,Matrix,Re=ModelX
if 0: #show kmeansort figure
    TM.kmeanSortFigure(Matrix,Re)
if 0: # open averageSort
    Pvalues=TM.averageSort(Matrix,Re)
if 0:
    flagOk1=[ [1,[2]], ] ;flagOk2=[ [1, [3]] ]  
    flagNot1=[ [1, [1, 3]] ] ;flagNot2=[ [6, [1,3]] ]  
    ReOk1=TM.hmmTestCertainOk(Matrix,flagOk1)
    ReOk2=TM.hmmTestCertainOk(Matrix,flagOk2)
    ReNot1=TM.hmmTestCertainNot(Matrix,flagNot1)
    ReNot2=TM.hmmTestCertainNot(Matrix,flagNot2)
    plt.figure(figsize=(25,12))
    plt.subplot(2,2,1)
    TM.ReFig([Re[ReOk1>0],Re[ReOk2>0],Re[ReNot1>0],Re[ReNot2>0],],['SelectOk1','SelectOk2','SelectNot1','SelectNot2'])
    plt.subplot(2,2,2)
    TM.ReFig([Re[(ReOk1>0)*(ReOk2>0)],Re[(ReOk1>0)*(ReNot1>0)],Re[(ReOk1>0)*(ReNot2>0)],Re[(ReOk2>0)*(ReNot1>0)],Re[(ReOk2>0)*(ReNot2>0)],Re[(ReNot1>0)*(ReNot2>0)],],\
                 ['Ok1-Ok2','Ok1-Not1','Ok1-Not2','Ok2-Not1','Ok2-Not2','Not1-Not2'])
    plt.subplot(2,2,3)
    TM.ReFig([Re[(ReOk1>0)*(ReOk2>0)*(ReNot1>0)],Re[(ReOk1>0)*(ReOk2>0)*(ReNot2>0)],Re[(ReOk1>0)*(ReNot1>0)*(ReNot2>0)],Re[(ReOk2>0)*(ReNot1>0)*(ReNot2>0)]],\
                 ['Ok1-Ok2-Not1','Ok1-Ok2-Not2','Ok1-Not1-Not2','Ok2-Not1-Not2'])
    plt.subplot(2,2,4)
    TM.ReFig([Re[(ReOk1>0)*(ReOk2>0)*(ReNot1>0)*(ReNot2)>0]], ['Ok1-Ok2-Not1-Not2'])
    
x2=time.clock()
print('time elapse:%.1f minutes' %((x2-x1)/60))


    















