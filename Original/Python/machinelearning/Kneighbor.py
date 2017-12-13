# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 14:34:40 2017

@author: Administrator 从2010年到2017年，每三年数据测试最近一年数据；
"""

from sklearn.neighbors import KNeighborsClassifier
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt

objectTrade='000001'

def Get_XY(startDate,endDate):
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

class knnDIY():
    def __init__(self,kneighbor):
        self.kneighbor=kneighbor
    def fit(self,trainX,Y):
        self.trainX=np.array(trainX)
        self.Y=np.array(Y)
    def predict(self,testX):
        labels=[]
        for i in range(len(testX)):
            euclidean_distance=np.linalg.norm(np.array(self.trainX)-np.array(testX[i]),axis=1)
            topN=np.argsort(euclidean_distance)[:self.kneighbor]  
            labels.append(int(np.mean(self.Y[topN])>0.5))
#            labels.append(int(np.mean(self.Y[topN])>0.5))
        return labels


#X,ReY=Get_XY('2014-01-01','2017-01-01')
#knn=KNeighborsClassifier(n_neighbors=5)
#knn.fit(X,ReY>0)
#
#X,ReY=Get_XY('2017-01-01','2017-12-01')
#labels=knn.predict(X)
#labelsU=[0,1]
#Fig(labels,labelsU,ReY)

X,ReY=Get_XY('2014-01-01','2017-01-01')
knn=knnDIY(5)
knn.fit(X,ReY>0)

X,ReY=Get_XY('2017-01-01','2017-12-01')
labels=knn.predict(X)
labelsU=np.unique(labels)
Fig(labels,labelsU,ReY)