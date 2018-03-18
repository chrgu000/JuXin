# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 16:56:10 2017

@author: Administrator
"""

from sklearn.cluster import KMeans
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.decomposition import PCA

objectTrade='000001'

def GetXY(startDate,endDate):
    global objectTrade
    data=ts.get_k_data(objectTrade,start=startDate,end=endDate,index=True)
    closes=np.array(data['close'])
    vols=np.array(data['volume'])
    opens=np.array(data['open'])
    highs=np.array(data['high'])
    lows=np.array(data['low'])

    tmp=closes[:-2]
    openNew=opens[1:-1]/tmp
    closeNew=closes[1:-1]/tmp
    highNew=highs[1:-1]/tmp
    lowNew=lows[1:-1]/tmp
    #volNew=vols[1:-1]/vols[:-2]
    ReY=closes[2:]/closes[1:-1]-1
    X=np.column_stack([openNew,closeNew,highNew,lowNew])

    return X,ReY

def Fig(labels,labelsU,ReY):
    Rlist=[];titles=[]
    for i in range(len(labelsU)):
        tem=labels==labelsU[i]
        Rlist.append(ReY[tem])
        titles.append('Label:'+str(labelsU[i]))
    plt.figure(figsize=(15,8))
    for i in range(len(titles)):
        plt.plot(Rlist[i].cumsum(),label=titles[i])
    plt.title(objectTrade)
    plt.legend()
    plt.grid()
    plt.show()

X,ReY=GetXY('2000-01-01','2013-01-01')
# X=(X-X.mean(axis=0))/X.std(axis=0)
scaler=preprocessing.StandardScaler()
X=scaler.fit_transform(X)
pca=PCA(0.8)
X=pca.fit_transform(X)
kmean=KMeans(n_clusters=4)
kmean.fit(X)
labels=kmean.labels_
labelsU=np.unique(labels)
Fig(labels,labelsU,ReY)

# loss=[] #通过肘型图测试K值选取问题；
# for i in range(2,12):
#     kmean=KMeans(n_clusters=i)
#     kmean.fit(X)
#     loss.append(kmean.inertia_)
# plt.plot(list(range(2,12)),loss)
# plt.grid()
# plt.show()

X,ReY=GetXY('2013-01-01','2017-12-01')
X=scaler.transform(X)
X=pca.transform(X)
labels=kmean.predict(X)
Fig(labels,labelsU,ReY)





