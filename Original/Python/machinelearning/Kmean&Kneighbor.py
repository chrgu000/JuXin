# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:35:15 2017

@author: Administrator
"""


from hmmlearn.hmm import GaussianHMM
from matplotlib import cm
from sklearn.cluster import KMeans

import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import datetime


objectTrade='000001'

def GetXY(startDate,endDate):
    global objectTrade    
    data=ts.get_k_data(objectTrade,start=startDate,end=endDate,index=True)
    closes=np.array(data['close'])
    vols=np.array(data['volume'])
    
    ReX=(np.array(closes[1:-1])/np.array(closes[:-2]))[2:]
    ReMa5 = np.array([closes[i]/closes[i-3:i+1].mean() for i in range(3,len(closes)-1)])
    ratioV=np.array([vols[i]/vols[i-3:i+1].mean() for i in range(3,len(vols)-1)])
    ReY=closes[4:]/closes[3:-1]-1
    #ReX=[];ReMa5=[];ratioV=[];ReY=[]
    #for i in range(3,len(closes)-1):
    #    ReX.append(closes[i]/closes[i-1])
    #    ReMa5.append(closes[i]/closes[i-3:i+1].mean())
    #    ratioV.append(vols[i]/vols[i-3:i+1].mean())
    #    ReY.append(closes[i+1]/closes[i]-1)
    #ReX=np.array(ReX)
    #ReMa5=np.array(ReMa5)
    #ratioV=np.array(ratioV)
    #ReY=np.array(ReY)
    X = np.column_stack([ReX,ReMa5,ratioV])
    return X,ReY

def Get_XY(startDate,endDate):
    global objectTrade    
    data=ts.get_k_data(objectTrade,start=startDate,end=endDate,index=True)
    closes=np.array(data['close'])
    vols=np.array(data['volume'])
    opens=np.array(data['open'])
    highs=np.array(data['high'])
    lows=np.array(data['low'])

    ReX=[];ReMa5=[];ratioV=[];ReY=[]
    for i in range(3,len(closes)-1):
        tmp=closes[i-1]
        ReX.append([opens[i]/tmp,closes[i]/tmp,highs[i]/tmp,lows[i]/tmp])
        ReMa5.append(closes[i]/closes[i-3:i+1].mean())
        ratioV.append(vols[i]/vols[i-1])
        ReY.append(closes[i+1]/closes[i]-1)
    ReX=np.array(ReX)
    ReMa5=np.array(ReMa5)
    ratioV=np.array(ratioV)
    ReY=np.array(ReY)
    X = np.column_stack([ReX])
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
kmean=KMeans(n_clusters=3)
kmean.fit(X)
labels=kmean.labels_
labelsU=np.unique(labels)
Fig(labels,labelsU,ReY)

X,ReY=GetXY('2015-01-01','2017-12-01')
labels=kmean.predict(X)
Fig(labels,labelsU,ReY)

#from sklearn.neighbors import KNeighborsClassifier # for Kneighbor
#X,ReY=Get_XY('2014-01-01','2017-01-01')
#knn=KNeighborsClassifier(n_neighbors=5,p=2,metric='minkowski')
#knn.fit(X,ReY>0)
#
#X,ReY=Get_XY('2017-01-01','2017-12-01')
#labels=knn.predict(X)
#labelsU=[0,1]
#Fig(labels,labelsU,ReY)