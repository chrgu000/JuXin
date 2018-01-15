import numpy as np

Data=np.loadtxt('wine.txt')

def PCAdiy(Data,n):
    meanV=np.mean(Data,axis=0)
    dataNew=Data-meanV
    covMat=np.cov(dataNew,rowvar=0)
    eigVals,eigVects=np.linalg.eig(covMat)
    eigVindex=np.argsort(eigVals)[::-1]
    tmp=eigVindex[:n]

    eigVectSelected=eigVects[:,tmp]
    return eigVectSelected

print(Data.shape)
Vectors=PCAdiy(Data,3)
dataNew=np.dot(Data,Vectors)
print(dataNew.shape)






