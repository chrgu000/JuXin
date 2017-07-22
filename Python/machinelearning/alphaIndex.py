# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 11:33:27 2017

@author: Administrator
"""

from WindPy import *
import datetime
import numpy as np
import matplotlib.pyplot as plt


index='000300.SH'
selected=50
year=2010
month=0
w.start()
Date=datetime.date.today()
loops=(Date.year-year)*12+Date.month-1
#dataTem=w.wsd(index,'pct_chg',str(year)+'0101',datetime.datetime.strftime(Date,'%Y%m%d'),'Period=M','PriceAdj=F')
#yIndex=np.array(dataTem.Data[0][0:-1])/100
resultsV=[]
resultsP=[]
resultsIndex=[]
for i in range(loops):
    if month==12:
        year=year+1
        month=1
    else:
        month=month+1
    DateStart=str(year)+'-'+str(month)+'-01'    
    if month==12:
        DateEnd=str(year+1)+'-'+'01-01'
    else:
        DateEnd=str(year)+'-'+str(month+1)+'-01'   
    dataTem=w.wset('sectorconstituent','date='+DateStart+';windcode='+index)
    stocks=dataTem.Data[1]
    dataTem=w.wss(stocks,'total_shares,close,pe_ttm','tradeDate='+DateStart,'priceAdj=F','cycle=D','unit=1')
    shares=np.array(dataTem.Data[0])
    price=np.array(dataTem.Data[1])
    pe=np.array(dataTem.Data[2])
    values=shares*price
    
    indVal=values.argsort()
    indPe=pe.argsort()
    indSelected=[i for i in range(selected)]
#    L=len(stocks)
#    indSelected=[i for i in range(L-selected,L)]    
    
    priceV1=price[indVal[indSelected]]
    stocksS=np.array(stocks)[indVal[indSelected]].tolist()
    dataTem=w.wss(stocksS,'close','tradeDate='+DateEnd,'priceAdj=F','cycle=D')
    priceV2=np.array(dataTem.Data[0])
    upStockV=(priceV2/priceV1-1).mean()
    
    priceP1=price[indPe[indSelected]]
    stocksS=np.array(stocks)[indPe[indSelected]].tolist()
    dataTem=w.wss(stocksS,'close','tradeDate='+DateEnd,'priceAdj=F','cycle=D')
    priceP2=np.array(dataTem.Data[0])
    upStockP=(priceP2/priceP1-1).mean()
    
    dataTem=w.wss(index,'close','tradeDate='+DateStart,'priceAdj=F','cycle=D')
    priceI1=dataTem.Data[0][0]
    dataTem=w.wss(index,'close','tradeDate='+DateEnd,'priceAdj=F','cycle=D')
    priceI2=dataTem.Data[0][0]
    upIndex=priceI2/priceI1-1
    
    resultsV.append(upStockV-upIndex)
    resultsP.append(upStockP-upIndex)
    resultsIndex.append(upIndex)

yV=np.array(resultsV)
yP=np.array(resultsP)
yIndex=np.array(resultsIndex)
plt.plot(yV.cumsum(),label='TotalValue')
plt.plot(yP.cumsum(),label='PeTTM')
plt.plot(yIndex.cumsum(),label=index)
plt.legend(loc='upper left', bbox_to_anchor=(0,1.15),ncol=3,fancybox=True,shadow=True)
plt.grid()



    
    
    
    
    
    
    
    
    
    
    
    
    
