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

class kmeanDIY():
    def __init__(self,kcentroids):
        self.n=kcentroids
        
    def fit(self,X):
        X=np.array(X)
        
        rowX,colX=X.shape#----------------初始化中心
        
        
#        centroids=np.zeros([self.n,colX])
#        for i in range(self.n):
#            tmp=X[:,i]
#            centroids[:,i]=min(tmp)+(max(tmp)-min(tmp))*np.random.rand(self.n)
        #----------------------------------------------------------------------------
        centroids=[]
        centroids.append(X[np.random.randint(0,rowX,1)[0],:].tolist())
        for i in range(self.n-1):
            iDist=[]
            for i2 in range(rowX):
#                pdb.set_trace()
                if len(centroids)<2:
                    tmp=np.linalg.norm(np.array(centroids)-X[i2,:])
                    tmp=[tmp]
                else:

                    tmp=np.linalg.norm(np.array(centroids)-X[i2,:],axis=1)
                if np.min(tmp)>0.000001:
                    iDist.append(np.min(tmp))
                else:
                    iDist.append(np.inf)
            tmp=np.argmin(iDist)
            centroids.append(X[tmp,:].tolist())
        centroids=np.array(centroids)
        
        clusterP=np.zeros([rowX,2])# 第一列计算归属哪一中心，第二列距离
        changed=True
        while changed:
            changed=False
            for i in range(rowX):
                iCent=0
                iDist=np.linalg.norm(X[i,:]-centroids[0,:])
                for i2 in range(1,self.n):
                    tmp=np.linalg.norm(X[i,:]-centroids[i2,:])
                    if tmp<iDist:
                        iCent=i2
                        iDist=tmp                
                if clusterP[i,0]!=iCent:
                    changed=True
                    clusterP[i,:]=iCent,iDist
        
        self.labels_=clusterP[:,0]
        self.centroids=centroids
        
    def predict(self,X):
        labels=[]
        for i in range(X.shape[0]):
            tmp=np.linalg.norm(self.centroids-X[i,:],axis=1)
            labels.append(np.argmin(tmp))
        return labels
                
X,ReY=GetXY('2000-01-01','2013-01-01')
#scaler=preprocessing.StandardScaler()
#X=scaler.fit_transform(X)
#pca=PCA(0.9)
#X=pca.fit_transform(X)
kmean=KMeans(n_clusters=3)
kmean.fit(X)
labels=kmean.labels_
labelsU=np.unique(labels)
Fig(labels,labelsU,ReY)

X,ReY=GetXY('2013-01-01','2017-12-01')
#X=scaler.transform(X)
#X=pca.transform(X)
labels=kmean.predict(X)
Fig(labels,labelsU,ReY)

#X,ReY=GetXY('2008-01-01','2015-01-01')
#kmean=kmeanDIY(3)
#kmean.fit(X)
#labels=kmean.labels_
#labelsU=np.unique(labels)
#Fig(labels,labelsU,ReY)
#
#X,ReY=GetXY('2015-01-01','2017-12-01')
#labels=kmean.predict(X)
#Fig(labels,labelsU,ReY)
        
        
















