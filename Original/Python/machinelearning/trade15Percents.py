# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 10:43:25 2018

@author: Administrator
"""

import tushare as ts
import pymysql
import talib
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
import xgboost

conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
cur=conn.cursor()
conn.select_db('pythonStocks')     
Lstocks=cur.execute('select number from stocks') # select name from stocks: get stocks' name;
Number=np.insert(np.cumsum(cur.fetchall()),0,0)
cur.execute('select name from stocks') # select name from stocks: get stocks' name;
stocks=cur.fetchall()
cur.execute('select * from dataDay') #'select * from dataDay limit '
dataAll=np.column_stack(cur.fetchall())
cur.close()
conn.close()


Lnum=len(Number)
profitIC=[]
profit=[]
fig=0
features=[]
#for i2 in range(10,30):
for i2 in range(Lnum-1):
    startT=Number[i2]
    endT=Number[i2+1]
    opens=dataAll[1][startT:endT].astype('float64')
    closes=dataAll[2][startT:endT].astype('float64')
    highs=dataAll[3][startT:endT].astype('float64')
    lows=dataAll[4][startT:endT].astype('float64')
    
    L=len(closes)
    hold=False
    holdP=0
    lastB=0
    threshhold=0.15
    threshholdx=0.15
    EMA=talib.EMA(closes,timeperiod=12)
    MACD,_,_=talib.MACD(closes,fastperiod=6,slowperiod=12,signalperiod=9)
    RSI=talib.RSI(np.array(closes),timeperiod=12)
    MOM=talib.MOM(np.array(closes),timeperiod=5)
    
    for i in range(19,L-1):
        if hold:
            high=max(highs[lastB:i+1])
            if (high-lows[i])/high>threshholdx:
                if opens[i]<high*(1-threshholdx):
                    currentP=opens[i]
                else:
                    currentP=high*(1-threshholdx)
                profit.append(currentP/holdP-1.004)
                hold=False
                lastB=i
                if fig>0:
                    fig=fig-1
                    plt.figure(figsize=(10,6))
                    ax=plt.subplot()
                    candleData=np.column_stack([list(range(len(closes[orderBar-1:i+1]))),\
                     opens[orderBar-1:i+1],highs[orderBar-1:i+1],lows[orderBar-1:i+1],closes[orderBar-1:i+1]])
                    mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
                    plt.plot([1,len(closes[orderBar-1:i+1])-1],[holdP,currentP])
        
        else:
            low=min(lows[lastB:i+1])
            if (highs[i]-low)/low>threshhold and low*(1+threshhold)<closes[i-1]*1.09:
                if opens[i]>low*(1+threshhold):
                    holdP=opens[i]
                else:
                    holdP=low*(1+threshhold)
                hold=True
                orderBar=i #record trading bar
                features.append([EMA[i],MACD[i],RSI[i],MOM[i]])
                
        if i>L-3 and hold:
            features.pop()
#            profit.append(closes[i]/holdP-1.004)
#            hold=False
#    if len(profit)>50:
#        profitIC.append(np.mean(profit)/np.std(profit))
#    else:
#        profitIC.append(-1)

#    plt.figure(figsize=(10,6))
#    plt.plot(np.cumsum(profit))

data_train=xgb.DMatrix(data=features[:130000],label=profit[:130000]>0);
data_test=xgb.DMatrix(data=features[130000:160000],label=profit[130000:160000]>0)
watch_list={(data_test,'eval'),(data_train,'train')}
param={'max_depth':3,'eta':0.03,'early_stopping_rounds':3,'silent':1,'objective':'multi:softmax','num_class':2}
XGB=xgb.train(param,data_train,num_boost_round=2000,evals=watch_list) #modeify 20000
data=xgb.DMatrix(data=features[160000:])
k=XGB.predict(data)

















