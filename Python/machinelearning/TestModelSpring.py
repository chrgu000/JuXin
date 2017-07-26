# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:38:05 2017

@author: Caofa
"""

from sklearn.cross_validation import train_test_split
from hmmlearn.hmm import GaussianHMM
from WindPy import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import pickle,joblib

sw1=0 # load data from .mat file,calculate model data adn save it;
sw2=0 # train hmm model
sw3=1 # test hmm model
fileSave='D:\Trade\Python\machinelearning\modelTestSpring'

if sw1:
    Tem=sio.loadmat('d:\\Trade\\allStocks1.mat')
    stocks=Tem['stocks']
    Date=Tem['Date']
    Opens=Tem['opens']
    Closes=Tem['closes']
    Tem=sio.loadmat('d:\\Trade\\allStocks2.mat')
    Highs=Tem['highs']
    Lows=Tem['lows']
    Tem=sio.loadmat('d:\\Trade\\allStocks3.mat')
    Vols=Tem['vols']
    Turns=Tem['turns']
    
    Rall=[];dateAll=[];Matrix=[];Matrix=[]
    Lstocks=len(stocks)
    for i in range(Lstocks):
        Open=Opens[:,i];Close=Closes[:,i];High=Highs[:,i];Low=Lows[:,i];Vol=Vols[:,i];date=Date
        Tem=sum(np.isnan(Open))
        Open=Open[Tem:];Close=Close[Tem:];High=High[Tem:];Low=Low[Tem:];Vol=Vol[Tem:];date=date[Tem:]
        Li=len(High)
        for i2 in range(10,Li-5):
            if Close[i2-1]<Low[i2-1]+(High[i2-1]-Low[i2-1])*0.25 and Close[i2]/Close[i2-1]<1.095 and High[i2]>Low[i2] \
            and 1.025 <=Close[i2]/Close[i2-1]<1.055 and Low[i2]/Low[i2-1]>=1.01:
                Rall.append(Close[i2+2]/Close[i2]-1)
                dateAll.extend(date[i2][0].tolist())
                Matrix.append([ np.std([Close[i2],Open[i2],Low[i2],High[i2]])/np.std([Close[i2-1],Open[i2-1],Low[i2-1],High[i2-1]]),\
                                     np.mean(Close[i2-3:i2+1])/np.mean(Close[i2-10:i2+1]),High[i2]/High[i2-1],Close[i2]/Low[i2-1],Close[i2]/High[i2-1] ])
    Tem=open(fileSave,'wb')
    tem={'Rall':Rall,'dateAll':dateAll,'Matrix':Matrix}
    pickle.dump(tem,Tem)
    Tem.close()

Tem=open(fileSave,'rb')
tem=pickle.load(Tem)
Tem.close()
Rall=tem['Rall'];dateAll=tem['dateAll'];Matrix=tem['Matrix']
X = np.row_stack(Matrix)
X,X0,Re,y0=train_test_split(X,np.array(Rall),test_size=0.0)
Lindicators=X.shape[1]
#    for i in range(Lindicators):
#        Mark='indicator:'+str(i+1)
#        hmmTestAll(np.row_stack(X[:,i]),Re,Mark)   
if sw2:    
    hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=10000).fit(X) #spherical,diag,full,tied 
    joblib.dump(hmm,fileSave+'HMM')
    
    flag=hmm.predict(X) 
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
    plt.xlabel('All Sorts',fontsize=16)
    plt.legend(loc='upper left')
    plt.grid(1)    
      
elif sw3:       
    hmm=joblib.load(fileSave+'HMM')
    flag=hmm.predict(X) 
    buy=(flag==0)+(flag==2)+(flag==4)+(flag==15)
    sell=(flag==0)+(flag==3)+(flag==4)+(flag==5)
    plt.figure(figsize = (15,8))
    ReT=Re[buy]
    ReTcs=ReT.cumsum()
    LT=len(ReT)
    maxDraw=0
    xi=0
    yi=0
    i2High=0
    for i2 in range(LT):
        if ReTcs[i2]>i2High:
            i2High=ReTcs[i2]
        drawT=i2High-ReTcs[i2]
        if maxDraw<drawT:
            maxDraw=drawT
            xi=i2
            yi=ReTcs[i2]
    plt.plot(range(LT),ReTcs,label='latent_state %s;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
             %('Selected',LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))
    plt.plot(xi,yi,'r*')
    plt.legend(loc='upper left')
    plt.grid(1) 
    
    
    
    


    


        
        
    
    


        
            

    
        
































