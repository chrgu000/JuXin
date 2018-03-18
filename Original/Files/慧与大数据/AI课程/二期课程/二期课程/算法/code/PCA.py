import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

def PCAdiy(Data,n):
    meanV = np.mean(Data, axis=0) # 取均值
    dataNew=Data-meanV #减去均值，归零化
    covMat=np.cov(dataNew,rowvar=0) # 0 代表一行为一个样本，非零代表一列为一个样本
    eigVals,eigVects=np.linalg.eig(covMat) #求特征值特征向量
    eigVindex = np.argsort(eigVals)[::-1] #对特征值排序并返回排序后的索引值（降序）；
    if n<1:
        eigTmp = eigVals[eigVindex]
        Values = eigTmp.cumsum()
        ValuesPercents = Values / sum(eigTmp)
        n=sum(ValuesPercents<n)+1
    eigVindexSelect = eigVindex[:n] #选取eigVals的Top n 的索引；
    eigVectSelect=eigVects[:,eigVindexSelect]  #选取eigVals的Top n对应的eigVectors；

    return eigVectSelect

Data=np.loadtxt('wine.txt')
# X = (X - X.mean(axis=0)) / X.std(axis=0)
sc=preprocessing.StandardScaler() #标准化 等同于Z-score
Data=sc.fit_transform(Data) #标准化
vectors=PCAdiy(Data,0.6)
dataNew=np.dot(Data,vectors)
plt.scatter(dataNew[:,0],dataNew[:,1])
plt.show()




