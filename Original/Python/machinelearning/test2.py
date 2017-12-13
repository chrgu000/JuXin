# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 09:53:48 2017

@author: Administrator
"""

import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing

objectTrade='000001'

def GetXY(startDate,endDate):
    global objectTrade    
    data=ts.get_k_data(objectTrade,start=startDate,end=endDate,index=True)
    closes=np.array(data['close'])
    vols=np.array(data['volume'])
    opens=np.array(data['open'])
    highs=np.array(data['high'])
    lows=np.array(data['low'])

#    ReX=[];ReY=[]
#    for i in range(1,len(closes)-1):
#        tmp=closes[i-1]
#        ReX.append([opens[i]/tmp,closes[i]/tmp,highs[i]/tmp,lows[i]/tmp])
#        ReY.append(closes[i+1]/closes[i]-1)
#    ReX=np.array(ReX)
#    ReMa5=np.array(ReMa5)
#    ratioV=np.array(ratioV)
#    ReY=np.array(ReY)
#    X = np.column_stack([ReX])    
    tmp=closes[:-2]
    openNew=opens[1:-1]/tmp
    closeNew=closes[1:-1]/tmp
    highNew=highs[1:-1]/tmp
    lowNew=lows[1:-1]/tmp   
    ReY=closes[2:]/closes[1:-1]-1
    X=np.column_stack([openNew,closeNew,highNew,lowNew])
    return X,ReY

def Fig(labels,labelsU,ReY):
    Rlist=[];titles=[];
    for i in range(len(labelsU)):
        tem=labels==labelsU[i]
        Rlist.append(ReY[tem])
        titles.append('Label:'+str(i))
    plt.figure(figsize=(15,8))    
    for i in range(len(titles)):
        plt.plot(Rlist[i].cumsum(),label=titles[i])
    plt.title(objectTrade)
    plt.legend()
    plt.grid()

                
X,ReY=GetXY('2010-01-01','2015-01-01')
scaler=preprocessing.StandardScaler()
X=scaler.fit_transform(X)
clf=MLPClassifier(solver='adam',learning_rate='adaptive',hidden_layer_sizes=(12,8),activation='tanh')
tmp=np.ones(len(ReY))
tmp[ReY>0.005]=2
tmp[ReY<-0.005]=0
kk=clf.fit(X,tmp)

labels=clf.predict(X)
labelsU=np.unique(labels)
Fig(labels,labelsU,ReY)

X,ReY=GetXY('2015-01-01','2017-12-01')
X=scaler.transform(X)
labels=clf.predict(X)
Fig(labels,labelsU,ReY)


        
        








































































