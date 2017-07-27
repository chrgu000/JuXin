# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:10:55 2017

@author: Administrator
"""


from hmmlearn.hmm import GaussianHMM
from seqlearn.perceptron import StructuredPerceptron
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import joblib, warnings

sw1=1 # test all for the first time
sw2=0 # show figure after delete some bad type (should be done by hand)
sw3=0 # test all for the second time after delete some bad type
sw4=0 # train by seq

warnings.filterwarnings("ignore")
fileSave='D:\\Trade\\Python\\machinelearning\\testHMM'
def hmmTestAll(Xraw,Reraw):
    Xshape=Xraw.shape
    Xrow=Xshape[0]
    Xcol=Xshape[1]
#    Xraw,X0,Re,y0=train_test_split(Xraw,np.array(Re),test_size=0.0)
    for lp in range(Xcol+1):
        if lp<Xcol:
            X=Xraw[:,lp]
            figTitle=str(lp)
        else:
            X=Xraw
            figTitle='All'
        trainSample=50000
        if Xrow<trainSample:
            Xtrain=X[:Xrow//2]
            Xtest=X[Xrow//2:]
            Retrain=Reraw[:Xrow//2]
            Retest=Reraw[Xrow//2:]
        else:
            Xtrain=X[:trainSample]
            Xtest=X[trainSample:]    
            Retrain=Reraw[:trainSample]  
            Retest=Reraw[trainSample:]
            
        hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=10000).fit(np.row_stack(Xtrain)) #spherical,diag,full,tied 
        joblib.dump(hmm,fileSave+figTitle)
        
#        for i in range(2):
        for i in range(1):
            i=1
            
            if i==0:
                Xtem=Xtrain
                Retem=Retrain
            else:
                Xtem=Xtest
                Retem=Retest
                
            flag=hmm.predict(np.row_stack(Xtem))
            plt.figure(figsize=(15,8))
            xi=[]
            yi=[]
            for i2 in range(hmm.n_components):
                state=(flag==i2)
                ReT=Retem[state]
                ReTcs=ReT.cumsum()
                LT=len(ReT)
                if LT<2:
                    continue
                maxDraw=0
                maxDrawi=0
                maxDrawValue=0
                i2High=0
                for i3 in range(LT):
                    if ReTcs[i3]>i2High:
                        i2High=ReTcs[i3]
                    drawT=i2High-ReTcs[i3]
                    if maxDraw<drawT:
                        maxDraw=drawT
                        maxDrawi=i3
                        maxDrawValue=ReTcs[i3]
                xi.append(maxDrawi)
                yi.append(maxDrawValue)  
                plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                         %(i2,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
            plt.plot(xi,yi,'r*')
            plt.title(figTitle,fontsize=16)
    #        plt.legend(loc='upper',bbox_to_anchor=(0.0,1.0),ncol=1,fancybox=True,shadow=True)
            plt.legend(loc='upper left')
            plt.grid(1)    
       

def hmmTestCertain(Matrix,Re,flagSelected):
    X=np.row_stack(Matrix)  
    def hmmTCi(paraList): #Nind -- which indicator; flaNot -- not which flag for this indicator;
        Nind=[]
        flagNot=[]
        for i in range(len(paraList)):
            Nind.append(paraList[i][0])
            flagNot.append(paraList[i][1])            
        flag=np.ones(len(X))>0
        for i2 in range(len(Nind)):    
            hmm=joblib.load(fileSave+str(Nind[i2]))
            flagTem=hmm.predict(np.row_stack(X[:,Nind[i2]]))
            for i in range(len(flagNot[i2])):
                    flag=flag*(flagTem!=flagNot[i2][i])       
        return flag
    
    flag=hmmTCi(flagSelected)

    ReT=Re[flag]
    ReTcs=ReT.cumsum()
    LT=len(ReT)
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
    plt.figure(figsize=(15,8))
    plt.plot(range(LT),ReTcs,label='latent_state: %s;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
             %('Selected',LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
    plt.plot(maxDrawi,maxDrawValue,'r*')
    plt.legend(loc='upper left')
    plt.grid(1) 
    return flag
               
if sw1:
    fileName='E:\Trade\R_Matrix'
    tem=sio.loadmat(fileName)
    Matrix=tem['Matrix'] 
    Rall=tem['Rall']
    tem=[]
    Re=Rall[:,1] #0:return1; 1:return2 
    hmmTestAll(Matrix,Re)    
if sw2:
    flagSelected=[ [2,[0]],[3,[3]],[4,[2]],[6,[3,4]],[7,[1,3]],[8,[3]],[9,[3]],\
                  [10,[0,3]],[11,[2]],[13,[1]],[14,[2]],[15,[4]],[16,[0,2]],[21,[2]],[24,[0]] ]
    flag=hmmTestCertain(Matrix,Re,flagSelected) 
if sw3:
    Matrix=Matrix[flag,:] 
    Re=Re[flag]
    hmmTestAll(Matrix[:,[0,1,3,9,10,11,14,15,17,23,24,25]],Re)
    #hmmTestAll(Matrix,Re)
if sw4:
    




    



