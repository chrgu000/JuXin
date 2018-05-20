# -*- coding: utf-8 -*-
"""
Created on Tue May 15 14:53:56 2018

@author: Administrator
"""

import tushare as ts
import numpy as np
#import xgboost as xgb
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import datetime,time,shutil,os,pickle,pdb
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

saveFolder='E:\\youdao\\'
today=datetime.date.today()
try:
    tmp=open('E:\\youdao.pkl','rb')
    pklData=pickle.load(tmp)
    tmp.close()
    daySave=pklData['today']
    if daySave<today:
        reload=1
    else:
        reload=0
        dataCall=pklData['dataCall']
        stocks=pklData['stocks']
        L=len(stocks)
except:
    reload=1
if reload:
    tmp=ts.get_stock_basics()
    stocks=tmp.index
    L=len(stocks)    
    t1=time.time()
    dataCall=[]
    dateBase=datetime.datetime.strptime('2018-03-01','%Y-%m-%d')
    for i in range(L):
        tmp=ts.get_k_data(code = stocks[i],start = '2017-01-01')
        dataCall.append(tmp)
        ratioStocks=(i+1)/L
        t2=time.time()
        print('loaded '+stocks[i]+':'+str(round(100*ratioStocks,2))+'%,and need more time:{} minutes'.format(round((t2-t1)*(1/ratioStocks-1)/60,2)))
    pklData={'dataCall':dataCall,'stocks':stocks,'today':today}
    tmp=open('E:\\youdao.pkl','wb')
    pickle.dump(pklData,tmp)
    tmp.close()
try:
    shutil.rmtree(saveFolder)
except:
    pass
os.mkdir(saveFolder)
tmp=ts.trade_cal()
tradeAll=tmp.calendarDate[tmp.isOpen>0].values
t1=time.time()
for i in range(L):
    datai=dataCall[i]
    if len(datai):
        dates=datai.date.values
        dateAll=[]
        Ldate=len(dates)
        for i2 in range(Ldate):
            dateAll.append(datetime.datetime.strptime(dates[i2],'%Y-%m-%d'))
        dateAll=np.array(dateAll)
        indTmp=sum(dateAll<dateBase)
        if indTmp==0:
            indTmp+=1
        for i2 in range(indTmp,Ldate):
            if np.where(tradeAll==dates[i2])[0][0]-np.where(tradeAll==dates[i2-1])[0][0]>1 and \
            datai.close[i2]/datai.close[i2-1]<0.99:
                if i2-5<0:
                    startBar=0
                else:
                    startBar=i2-5
                if i2+15>Ldate-1:
                    endBar=Ldate-1
                else:
                    endBar=i2+5
                fig=plt.figure(figsize=(10,6))
                ax=fig.add_axes([0.1,0.3,0.8,0.6])
                datai2=dataCall[i].loc[startBar:endBar].reset_index(drop=True)
                candleData=np.column_stack([range(len(datai2)),datai2.open,datai2.high,datai2.low,datai2.close])
                dateTmp=datai2.date
                volTmp=datai2.volume
                if startBar<1:
                    tmp=i2
                else:
                    tmp=5
                ax.text(tmp,datai2.high[tmp],'复盘日',fontsize=20,color='b')
                mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
                plt.title(stocks[i])
                indTmp=[0,5,len(dateTmp)-1]
                ax.set_xticks(indTmp)
                ax.grid()
                ax1=fig.add_axes([0.1,0.1,0.8,0.2])
                ax1.bar(range(len(volTmp)),volTmp)
                ax1.set_xticks(indTmp)
                ax1.set_xticklabels(dateTmp[indTmp],rotation=40)
                ax1.grid()
                plt.savefig(saveFolder+stocks[i]+'_复盘日：'+dateTmp[5])
                plt.clf()
    t2=time.time()
    ratioStocks=(i+1)/L
    print('Draw figures--'+stocks[i]+':'+str(round(100*ratioStocks,2))+'%,and need more time:{} minutes'.format(round((t2-t1)*(1/ratioStocks-1)/60,2)))




























