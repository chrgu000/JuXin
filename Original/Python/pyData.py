# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 10:00:29 2017

@author: Administrator
"""
import os
import tushare as ts
import numpy as np
import pandas as pd
import scipy.io as scio

dataFile='D:\pyData.mat'
data=scio.loadmat(dataFile)
os.remove(dataFile)
stocks=data['stocks'][0]
indicators=data['indicators'][0]
try:
    stocks=stocks.split(',')
except  Exception,e:
    print Exception,':',e

try:
    indicators=indicators.split(',')
except  Exception,e:
    print Exception,':',e
timeStart=data['timeStart'][0]
timeEnd=data['timeEnd'][0]
index=data['index'][0]
index=True if index>0 else False

if len(stocks)<2:
    if cmp(stocks[0].upper(),'ALL')>-1:
        dataTem=ts.get_stock_basics()
        stocks=dataTem.index
numStocks=len(stocks)
numIndicators=len(indicators)
dataTem = ts.get_k_data('000001', index=True,start=timeStart,end=timeEnd)
Ldate=dataTem.shape[0]
dataOpen=pd.DataFrame(columns=stocks,index=np.arange(Ldate))
dataClose=pd.DataFrame(columns=stocks,index=np.arange(Ldate))
dataHigh=pd.DataFrame(columns=stocks,index=np.arange(Ldate))
dataLow=pd.DataFrame(columns=stocks,index=np.arange(Ldate))
dataVolume=pd.DataFrame(columns=stocks,index=np.arange(Ldate))

for i in range(numStocks):
    dataTem=ts.get_k_data(stocks[i],index=index,start=timeStart,end=timeEnd)
    dataOpen.iloc[:, i] = dataTem.iloc[:, 1] # 将dataframe格式转换成list格式再赋值；
    dataClose.iloc[:, i] = dataTem.iloc[:, 2]
    dataHigh.iloc[:, i] = dataTem.iloc[:, 3]
    dataLow.iloc[:, i] = dataTem.iloc[:, 4]
    dataVolume.iloc[:, i] = dataTem.iloc[:, 5]
#data['x'].tolist()
fileTem='D:\pyData.xlsx'
writerTem=pd.ExcelWriter(fileTem,engine='xlsxwriter')
if 'open' in indicators:
    dataOpen.to_excel(writerTem,'open')
if 'close' in indicators:
    dataClose.to_excel(writerTem,'close')
if 'high' in indicators:
    dataHigh.to_excel(writerTem,'high')
if 'low' in indicators:
    dataLow.to_excel(writerTem,'low')
if 'volume' in indicators:
    dataVolume.to_excel(writerTem,'volume')
writerTem.save()


#dict(zip(x,y))





