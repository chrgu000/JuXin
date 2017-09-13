from WindPy import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import datetime,TrainModel

obj='IF.CFE'
nClusters=9

TM=TrainModel.TrainModel('test')
yesterday=datetime.date.today()-timedelta(days=1)
w.start()
data=w.wsd(obj,'open,high,low,close,volume',yesterday-timedelta(days=360*10),yesterday,'Fill=Previous','PriceAdj=F')
tem=~np.isnan(data.Data[0])
Matrix=np.column_stack(data.Data)[tem,:]
dates=np.array(data.Times)[tem]
opens=Matrix[:,0]
highs=Matrix[:,1]
lows=Matrix[:,2]
closes=Matrix[:,3]
vols=Matrix[:,4]
Re=closes[1:]/closes[:-1]-1 # from 0:-1 without the last one;
Matrix=Matrix[1:-1,:]/np.c_[np.tile(Matrix[0:-2,3],[4,1]).T,Matrix[0:-2,4]]
Re=Re[1:]
dates=dates[1:-1]

tem=np.isfinite(Matrix[:,-1])
Matrix=Matrix[tem,:]
Re=Re[tem]
dates=dates[tem]

clf=KMeans(n_clusters=nClusters)
clf.fit(Matrix)
labels=clf.labels_
labelsU=np.unique(labels)
Rlist=[];titles=[];
for i in range(len(labelsU)):
    tem=labels==labelsU[i]
    Rlist.append(Re[tem])
    titles.append('flags:'+str(i))
plt.figure(figsize=(15,8))
TM.ReFig(Rlist,titles)

pca=PCA(n_components='mle')
newMatrix=pca.fit_transform(Matrix) 
clf.fit(newMatrix)
labels=clf.labels_
labelsU=np.unique(labels)
Rlist=[];titles=[];
for i in range(len(labelsU)):
    tem=labels==labelsU[i]
    Rlist.append(Re[tem])
    titles.append('flagsNew:'+str(i))
plt.figure(figsize=(15,8))
TM.ReFig(Rlist,titles)


