# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 15:05:39 2017

@author: Administrator
"""

from WindPy import *
import matplotlib.pyplot as plt
import numpy as np
import time,pickle,pdb

try:
    dd
    tem=open('arbitrage50ETF.pkl','rb')
    data=pickle.load(tem)
    tem.close()
    Date=data['Date']
    Diff=data['Diff']
except:       
    today=time.strftime('%Y-%m-%d')
    w.start()
    tem=w.wsd('510050.sh','close','2005/2/23',today)
    dates=tem.Times
    dates=[i.strftime('%Y-%m-%d') for i in dates]
    P50etf=tem.Data[0]
    Lt=len(dates)
    Date=[]
    Diff=[]
    for i in range(Lt):
        tem=w.wset('etfconstituent','date='+dates[i]+';windcode=510050.OF')    
        shares=np.array(tem.Data[3])
        cashRatio=tem.Data[5]
        cashFix=tem.Data[6]
        if np.all(np.isfinite(shares) * (shares>0)):
            print(dates[i],end=',')
            stocks=tem.Data[1]
            stocks.append('510050.SH')
            tem=w.wss(stocks,'close','tradeDate='+dates[i],'cycle=D','priceAdj=U')
            Ptem=np.array(tem.Data[0])
            Date.append(dates[i])
#            pdb.set_trace()
            V_50etf=Ptem[-1]*1000000
            V_stocks=Ptem[:-1]*shares
            for i2 in range(len(stocks)-1):
                if cashRatio[i2] == None:
                    if cashFix[i2]!=None:
                        V_stocks[i2]=V_stocks[i2]+cashFix[i2] 
                else:
                    V_stocks[i2]=V_stocks[i2]*(1+cashRatio[i2]/100)
            Diff.append(V_50etf-sum(V_stocks))

    data={'Date':Date,'Diff':Diff}
    tem=open('arbitrage50ETF.pkl','wb')
    pickle.dump(data,tem)
    tem.close()
    
plt.figure(figsize=(15,8))
plt.plot(Diff)
ax=plt.gca()
tem=list(map(int,np.linspace(0,len(Date),18)))
tem[-1]=tem[-1]-1
ax.set_xticks(tem)
tem=np.array(Date)[tem]
ax.set_xticklabels(tem,rotation=60)
plt.grid()
    






