# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:10:55 2017

@author: Administrator
"""


from hmmlearn.hmm import GaussianHMM
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio

def hmmTestAll(X,Re):
    Lt=X.shape
    Lt=Lt[0]
    X,X0,Re,y0=train_test_split(X,np.array(Re),test_size=0.0)
    trainSample=50000
    if Lt<trainSample:
        Xtrain=X[:Lt/2]
        Xtest=X[Lt/2:]
        Retrain=Re[:Lt/2]
        Retest=Re[Lt/2:]
    else:
        Xtrain=X[:trainSample]
        Xtest=X[trainSample:]    
        Retrain=Re[:trainSample]  
        Retest=Re[trainSample:]
        
    hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=1000).fit(Xtrain) #spherical,diag,full,tied 
#    joblib.dump(hmm,fileSave+'HMM')
    
    for i in range(2):
        if i==0:
            Xtem=Xtrain
            Re=Retrain
        else:
            Xtem=Xtest
            Re=Retest
            
        flag=hmm.predict(Xtem) 
        plt.figure(figsize=(15,8))
        xi=[]
        yi=[]
        for i in range(hmm.n_components):
            state=(flag==i)
            ReT=Re[state]
            ReTcs=ReT.cumsum()
            LT=len(ReT)
            if LT<2:
                continue
            maxDraw=0
            maxDrawi=0
            maxDrawValue=0
            i2High=0
            for i2 in range(LT):
                if ReTcs[i2]>i2High:
                    i2High=ReTcs[i2]
                drawT=i2High-ReTcs[i2]
                if maxDraw<drawT:
                    maxDraw=drawT
                    maxDrawi=i2
                    maxDrawValue=ReTcs[i2]
            xi.append(maxDrawi)
            yi.append(maxDrawValue)  
            plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                     %(i,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
        plt.plot(xi,yi,'r*')
#        plt.xlabel(Mark,fontsize=16)
        plt.legend(loc='upper left',bbox_to_anchor=(1.0,1.0),ncol=1,fancybox=True,shadow=True)
        plt.grid(1)    

fileName='E:\Trade\R_Matrix'
tem=sio.loadmat(fileName)
Matrix=tem['Matrix'] 
Rall=tem['Rall']
tem=[]
X=np.row_stack(Matrix[:,[3]])  #nice sort: 1 
Re=Rall[:,0]
#Mark='all indicators'
hmmTestAll(X,Re)
    



