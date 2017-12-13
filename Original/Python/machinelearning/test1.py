#import math
import numpy as np
import pdb
#from matplotlib import pyplot
#from collections import Counter
#import warnings

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
            labels.append(int(np.mean(self.Y[topN])>0))
        return labels


if __name__=='__main__':
 
    X=[[1,2],[2,3],[3,1],[6,5],[7,7],[8,6]]
    Y=[1,1,1,0,0,0]
    newSample = [[3.5,5.2],[1,0],[7,9]]  
    knn=knnDIY(2)
    knn.fit(X,Y)
    label=knn.predict(newSample)
    print(label)
 
 
    

















































