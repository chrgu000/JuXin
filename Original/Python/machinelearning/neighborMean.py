from WindPy import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.finance as mpf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime,TrainModel

obj='000001.sh'
nClusters=7

TM=TrainModel.TrainModel('neighborMean')
yesterday=datetime.date.today()-timedelta(days=1)
w.start()
data=w.wsd(obj,'open,high,low,close,volume',yesterday-timedelta(days=360*20),yesterday,'Fill=Previous','PriceAdj=F')
tem=~np.isnan(data.Data[0])
MatrixRaw=np.column_stack(data.Data)[tem,:]
dates=np.array(data.Times)[tem]
opens=MatrixRaw[:,0]
highs=MatrixRaw[:,1]
lows=MatrixRaw[:,2]
closes=MatrixRaw[:,3]
vols=MatrixRaw[:,4]
Re=closes[1:]/closes[:-1]-1 # from 0:-1 without the last one;
Matrix=MatrixRaw[1:-1,:]/np.c_[np.tile(MatrixRaw[0:-2,3],[4,1]).T,MatrixRaw[0:-2,4]]
Re=Re[1:]
dates=dates[1:-1];MatrixRaw=MatrixRaw[1:-1]

tem=np.isfinite(Matrix[:,-1])
Matrix=Matrix[tem,:]
Re=Re[tem]
dates=dates[tem];MatrixRaw=MatrixRaw[tem,:]

pca=PCA(n_components=0.98)
newMatrix=pca.fit_transform(Matrix) 
kmean=KMeans(n_clusters=nClusters)
#kmean.fit(newMatrix)
kmean.fit(Matrix[:,[0,3]])
labels=kmean.labels_
labelsU=np.unique(labels)
Rlist=[];titles=[];
for i in range(len(labelsU)):
    tem=labels==labelsU[i]
    Rlist.append(Re[tem])
    titles.append('flagsNew:'+str(i))
plt.figure(figsize=(15,8))
TM.ReFig(Rlist,titles)

plt.figure(figsize=(15,8))
ax=plt.subplot()
mpf.candlestick_ohlc(ax,np.c_[list(range(20)),MatrixRaw[:20,:4]],width=0.5,colorup='r',colordown='g')
plt.grid()

Lt=len(Matrix)
matrix=pd.DataFrame(Matrix[:,:4].T)
vols=Matrix[:,4].T
matrixCorr=matrix.corr()
Rtest=[]
for i in range(Lt):
    tem=(-matrixCorr[i]).argsort()[1:11]  
    if tem.sum()>2:
        if Re[tem].mean()>0.003:
            Rtest.append(Re[i])
plt.figure(figsize=(15,8))
TM.ReFig([Rtest],['test'])
    
    





























