# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 09:53:48 2017

@author: Administrator
"""

from hmmlearn.hmm import GaussianHMM
from WindPy import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

w.start()
objectTrade='000001.sh'

startDate='2005-06-01'
endDate='2017-9-22'
dataTem=w.wsd(objectTrade,'open,close,high,low',startDate,endDate,'PriceAdj=F')
tem=np.isnan(dataTem.Data[0])
opens=np.array(dataTem.Data[0])[~tem]
closes=np.array(dataTem.Data[1])[~tem]
highs=np.array(dataTem.Data[2])[~tem]
lows=np.array(dataTem.Data[3])[~tem]

Re1=[]
Re5=[]
ReDiff=[]
Re=[]
for i in range(5,len(opens)-2):
    Re1.append(closes[i]/closes[i-1])
    Re5.append(closes[i]/closes[i-5])
    ReDiff.append(highs[i]/lows[i])
    if closes[i+1]>closes[i]:
        Re.append(closes[i+2]/opens[i+1]-1.003)
    else:
        Re.append(opens[i+2]/opens[i+1]-1.003)
Re1=np.array(Re1)
Re5=np.array(Re5)
ReDiff=np.array(ReDiff)
Re=np.array(Re)
Lsplit=int(len(Re)*2/3)

train1=Re1[:Lsplit]
train2=Re5[:Lsplit]
train3=ReDiff[:Lsplit]
ReTrain=Re[:Lsplit]
test1=Re1[Lsplit:]
test2=Re5[Lsplit:]
test3=ReDiff[Lsplit:]
ReTest=Re[Lsplit:]

X = np.column_stack([train1,train2,train3])
hmm=GaussianHMM(n_components=3,covariance_type='diag',n_iter=100000).fit(X)
latent_states_sequence=hmm.predict(X)
plt.figure(figsize=(15,8))
for i in range(hmm.n_components):
    tem=ReTrain[latent_states_sequence==i]
    maxDrawBack=0
    temCS=tem.cumsum()
    for i2 in range(len(tem)):
        tem1=max(temCS[:i2+1])-temCS[i2]
        if tem1>maxDrawBack:
            maxDrawBack=tem1
    plt.plot(temCS,label='latent_state %d;orders:%d;IR:%.3f;winRatio:%.2f%%;maxDrawBack:%.2f%%;profitPer:%.2f%%' \
             %(i,len(tem),np.mean(tem)/np.std(tem),sum(tem>0)*100/len(tem),maxDrawBack*100,np.mean(tem)*100) )
plt.legend()
plt.grid(1)

        
X = np.column_stack([test1,test2,test3])
latent_states_sequence=hmm.predict(X)
plt.figure(figsize=(15,8))
for i in range(hmm.n_components):
    tem=ReTest[latent_states_sequence==i]
    maxDrawBack=0
    temCS=tem.cumsum()
    for i2 in range(len(tem)):
        tem1=max(temCS[:i2+1])-temCS[i2]
        if tem1>maxDrawBack:
            maxDrawBack=tem1
    plt.plot(temCS,label='latent_state %d;orders:%d;IR:%.3f;winRatio:%.2f%%;maxDrawBack:%.2f%%;profitPer:%.2f%%' \
             %(i,len(tem),np.mean(tem)/np.std(tem),sum(tem>0)*100/len(tem),maxDrawBack*100,np.mean(tem)*100) )
    #data['state %d_return'%i]=data.logReturn.multiply(idx,axis=0)
    #plt.plot(np.exp(data['state %d_return'%i].cumsum()),label='latent_state %d'%i)
plt.legend()
plt.grid(1)























