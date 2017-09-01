# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 08:59:29 2017

@author: Administrator
"""
import matlab.engine
import numpy as np
from sklearn import svm
from sklearn.neural_network import MLPClassifier

MatEng=matlab.engine.start_matlab()
MatEng.up4plusdown1PD_ML()

f=open('D:\Trading\up4plusdown1DataML.txt')
lines=f.readlines()
f.close()
L=len(lines)
X=[]
y=[]
for line in lines:
    raw=line.split(',')
    X.append(map(float,raw[:-1]))
    y.append(map(int,raw[-1][0])[0])
X=np.array(X)
y=np.array(y)
indTem=np.random.permutation(len(y))
X=X[indTem]
y=y[indTem]
Ltrain=int(len(y)*0.7)

clf_svm=svm.SVC()
clf_svm.fit(X[:Ltrain],y[:Ltrain])
yPredict=clf_svm.predict(X[Ltrain+1:])
results=yPredict==y[Ltrain+1:]
print "SVC:"
print float(results.sum())/len(yPredict)

clf_svm=svm.SVR()
clf_svm.fit(X[:Ltrain],y[:Ltrain])
yPredict=clf_svm.predict(X[Ltrain+1:])
yPredict=[1 if i>0.5 else 0 for i in yPredict]
results=yPredict==y[Ltrain+1:]
print "SVR:"
print float(results.sum())/len(yPredict)

clf_nueral=MLPClassifier(hidden_layer_sizes=[2],activation='logistic',random_state=3)
clf_nueral.fit(X[:Ltrain],y[:Ltrain])
yPredict=clf_nueral.predict(X[Ltrain+1:])
yPredict=[1 if i==True else 0 for i in yPredict]
results=np.array(yPredict)==np.array(y[Ltrain+1:])
print "neural_network:"
print float(np.array(results).sum())/len(yPredict)



