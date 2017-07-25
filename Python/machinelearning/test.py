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
import joblib, warnings
warnings.filterwarnings("ignore")

fileSave='testHMM'
def hmmTestAll(Xraw,Reraw):
    Xshape=Xraw.shape
    Xrow=Xshape[0]
    Xcol=Xshape[1]
#    Xraw,X0,Re,y0=train_test_split(Xraw,np.array(Re),test_size=0.0)
    for lp in range(Xcol):
        X=Xraw[:,lp]
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
        joblib.dump(hmm,fileSave+str(lp))
        
        for i in range(2):
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
    #        plt.xlabel(Mark,fontsize=16)
    #        plt.legend(loc='upper',bbox_to_anchor=(0.0,1.0),ncol=1,fancybox=True,shadow=True)
            plt.legend(loc='upper left')
            plt.grid(1)    
        
def hmmTestCertain(X,Re):
    hmm=joblib.load(fileSave+'1')
    flag1=hmm.predict(np.row_stack(X[:,3]))
    flag1=(flag1!=1)#*(flag1!=4)
    hmm=joblib.load(fileSave+'2')
    flag2=hmm.predict(np.row_stack(X[:,4]))
    flag2=flag2!=3
    hmm=joblib.load(fileSave+'3')
    flag3=hmm.predict(np.row_stack(X[:,7]))
    flag3=flag3!=2
    hmm=joblib.load(fileSave+'4')
    flag4=hmm.predict(np.row_stack(X[:,8]))
    flag4=flag4!=4
    hmm=joblib.load(fileSave+'5')
    flag5=hmm.predict(np.row_stack(X[:,9:11]))
    flag5=(flag5!=2)*(flag5!=4)
    hmm=joblib.load(fileSave+'6')
    flag6=hmm.predict(np.row_stack(X[:,12]))
    flag6=flag6!=1
    hmm=joblib.load(fileSave+'7')
    flag7=hmm.predict(np.row_stack(X[:,13]))
    flag7=flag7!=2
    hmm=joblib.load(fileSave+'8')
    flag8=hmm.predict(np.row_stack(X[:,15]))
    flag8=flag8!=3
    hmm=joblib.load(fileSave+'9')
    flag9=hmm.predict(np.row_stack(X[:,16]))
    flag9=flag9!=3
    hmm=joblib.load(fileSave+'10')
    flag10=hmm.predict(np.row_stack(X[:,17]))
    flag10=flag10!=0
    hmm=joblib.load(fileSave+'11')
    flag11=hmm.predict(np.row_stack(X[:,18]))
    flag11=flag11!=4
    flag=flag1*flag2*flag3*flag4*flag5*flag6*flag7*flag8*flag9*flag10*flag11
    
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
    plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
             %(100,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
    plt.plot(maxDrawi,maxDrawValue,'r*')
    plt.legend(loc='upper left')
    plt.grid(1) 
               

fileName='E:\Trade\R_Matrix'
tem=sio.loadmat(fileName)
Matrix=tem['Matrix'] 
Rall=tem['Rall']
tem=[]
Re=Rall[:,1] #0:return1; 1:return2 
hmmTestAll(Matrix,Re)             #nice sort1: 3,4,
#X=np.row_stack(Matrix)
#hmmTestCertain(X,Re)



    



