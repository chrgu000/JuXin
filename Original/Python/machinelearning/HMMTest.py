# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 09:53:48 2017

@author: Administrator
"""

from hmmlearn.hmm import GaussianHMM
from matplotlib import cm
from WindPy import *

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import datetime,joblib

w.start()
objectTrade='000001.sz'

startDate='2010-06-01'
endDate='2016-10-04'
dataTem=w.wsd(objectTrade,'close,high,low,volume',startDate,endDate,'PriceAdj=F')
close=dataTem.Data[0]
high=dataTem.Data[1][5:]
low=dataTem.Data[2][5:]
vol=dataTem.Data[3][5:]
money=dataTem.Data[3][5:]
dateList=pd.to_datetime(dataTem.Times[5:])
logReturn=(np.log(np.array(close[1:]))-np.log(np.array(close[:-1])))[4:]
logReturn5 = np.log(np.array(close[5:]))-np.log(np.array(close[:-5]))
diffReturn = (np.log(np.array(high))-np.log(np.array(low)))
closeidx = np.array(close[5:])
X = np.column_stack([logReturn,logReturn5,diffReturn])
hmm=GaussianHMM(n_components=3,covariance_type='diag',n_iter=100000).fit(X)
#joblib.dump(hmm,'HMMTest')
#hmm=joblib.load('HMMTest')
#startDate='2010-06-01'
#endDate='2017-7-5'
#dataTem=w.wsd(objectTrade,'close,high,low,volume',startDate,endDate,'PriceAdj=F')
#close=np.array(dataTem.Data[0])
#indTem=~np.isnan(close)
#close=close[indTem]
#high=np.array(dataTem.Data[1])[indTem]
#low=np.array(dataTem.Data[2])[indTem]
#vol=np.array(dataTem.Data[3])[indTem]
#money=np.array(dataTem.Data[3])[indTem]
#high=high[5:]
#low=low[5:]
#vol=vol[5:]
#money=money[5:]
#dateList=pd.to_datetime(np.array(dataTem.Times)[indTem][5:])
#logReturn=(np.log(np.array(close[1:]))-np.log(np.array(close[:-1])))[4:]
#logReturn5 = np.log(np.array(close[5:]))-np.log(np.array(close[:-5]))
#diffReturn = (np.log(np.array(high))-np.log(np.array(low)))
#closeidx = np.array(close[5:])
#X = np.column_stack([logReturn,logReturn5,diffReturn])

latent_states_sequence=hmm.predict(X)
sns.set_style('white')
plt.figure(figsize=(15,8))
for i in range(hmm.n_components):
    state=(latent_states_sequence==i)
    plt.plot(dateList[state],closeidx[state],'.',label='latent state %d' %i,lw=1)
plt.legend()
plt.grid(1)

data=pd.DataFrame({'dateList':dateList,'logReturn':logReturn,'state':latent_states_sequence}).set_index('dateList')
plt.figure(figsize=(15,8))
for i in range(hmm.n_components):
    state=(latent_states_sequence==i)
    idx=np.append(0,state[:-1])
    tem=data.logReturn.multiply(idx,axis=0)
    plt.plot(np.exp(tem.cumsum()),label='latent_state %d;orders:%d'%(i,sum(state)) )
    #data['state %d_return'%i]=data.logReturn.multiply(idx,axis=0)
    #plt.plot(np.exp(data['state %d_return'%i].cumsum()),label='latent_state %d'%i)
plt.legend()
plt.grid(1)

buy=(latent_states_sequence==0)#+(latent_states_sequence==1)+(latent_states_sequence==5)
buy=np.append(0,buy[:-1])
sell=(latent_states_sequence==0)+(latent_states_sequence==3)+(latent_states_sequence==4)+(latent_states_sequence==5)
sell = np.append(0,sell[:-1])
data['backTest_return'] = data.logReturn.multiply(buy,axis = 0)#- data.logReturn.multiply(sell,axis = 0)
plt.figure(figsize = (15,8))
plt.plot_date(dateList,np.exp(data['backTest_return'].cumsum()),'-',label='backtest result;orders:%d'%sum(buy))
plt.legend()
plt.grid(1)























