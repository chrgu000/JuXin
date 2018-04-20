# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:15:20 2018

@author: Administrator
"""
import tushare as ts
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import datetime,pickle,pdb,joblib

today=datetime.datetime.today()
#if 1: # only for the first time run
#    tmp=open('X-Scan.pkl','wb')
#    pklData={'dateSave':(today-datetime.timedelta(5)).date(),'profits':[],'stockTrade':[]}
#    pickle.dump(pklData,tmp)
#    tmp.close()    
    
tmp=open('X-Scan.pkl','rb')
pklData=pickle.load(tmp)
tmp.close()
fig=0
if (today.date()-pklData['dateSave']).days>0:
    tmp=ts.get_stock_basics()
    stocks=tmp.index
    L=len(stocks)
    nDays=50 #number of natural days;
    dataCall=[]
    for i in range(L):
        tmp=ts.get_k_data(code = stocks[i],start = datetime.datetime.strftime(today-datetime.timedelta(nDays),'%Y-%m-%d'))
        dataCall.append(tmp)
    #print('time lapse {} minutes.'.format(round((t2-today).seconds/60,2)))
    pklData['dateSave']=today.date()
    pklData['dataCall']=dataCall
    pklData['stocks']=stocks
    tmp=open('X-Scan.pkl','wb')
    pickle.dump(pklData,tmp)
    tmp.close()
    t2=datetime.datetime.now()
    print('Updating data has been completed now! and time lapses {} minutes.'.format(round((t2-today).seconds/60,2)))
elif 14<=today.hour<15 and today.minute>50 :
#else:
    stocks=pklData['stocks'].tolist()
    stockTrade=pklData['stockTrade']
    dataCall=pklData['dataCall']
        
    dataNow=ts.get_today_all()
    dataNow=dataNow.set_index('code')
    Lst=len(stockTrade) #close orders
    if Lst:
        todayT=today.date()
        for i in range(Lst):
            stocki=stockTrade[i]
            stockTmp=pklData[stocki]
            if dataNow.loc[stocki].low<=stockTmp[3]: #if touch stop loss
                if dataNow.loc[stocki].open<=stockTmp[3]:
                    stopReal=dataNow.loc[stocki].open
                else:
                    stopReal=stockTmp[3]
                pklData['profits'].append(stopReal/stockTmp[1]-1.004)
                pklData['stockTrade'].remove(stocki)
                del pklData[stocki]
            else:
                datei=dataCall[i].date.tolist()
                tmp=datei.index(datetime.datetime.strftime(stockTmp[0],'%Y-%m-%d'))
                holdDay=len(datei)-tmp+1
                if holdDay>=stockTmp[2]:
                    pklData['profits'].append(stopReal/stockTmp[1]-1.004)
                    pklData['stockTrade'].remove(stocki)
                    del pklData[stocki]
            tmp=open('X-Scan.pkl','wb')
            pickle.dump(pklData,tmp)
            tmp.close()
                
    features=[]
    stocksTarget=[]
    holds=[]
    openPrice=[]
    stopPrice=[]
    for i in range(len(stocks)):
        try:
            tmpNow=dataNow.loc[stocks[i]]
            opens=np.r_[dataCall[i].open, tmpNow.open]
            closes=np.r_[dataCall[i].close, tmpNow.trade]
            highs=np.r_[dataCall[i].high, tmpNow.high]
            lows=np.r_[dataCall[i].low, tmpNow.low]
            vols=np.r_[dataCall[i].volume, tmpNow.volume]
        except:
            continue
        Li=len(opens)-1
        for i2 in range(3,10):
            if Li-3*i2-5<0:
                break
            if closes[Li]/closes[Li-1]>1.092:
                continue                
            if abs(max(highs[Li-3*i2-1:Li-3*i2+2])-max(highs[Li-3*i2-5:Li-2*i2+2]))<0.00000001 and \
            abs(min(lows[Li-3*i2:Li-i2+1])-min(lows[Li-2*i2-1:Li-2*i2+2]))<0.00000001 and \
            abs(max(highs[Li-2*i2:Li+1])-max(highs[Li-i2-1:Li-i2+2]))<0.00000001 and \
            lows[Li]<min(lows[Li-i2:Li]) and \
            min(highs[Li-3*i2-5:Li+1]-lows[Li-3*i2-5:Li+1])>0.0000001:
                P1=np.argmax(highs[Li-3*i2-5:Li-2*i2+1]) #index 0 is i-3*i2-5
                P2=np.argmin(lows[Li-2*i2-1:Li-2*i2+2])+i2+4
                P3=np.argmax(highs[Li-i2-1:Li-i2+2])+2*i2+4
                P4=3*i2+5
                down1=P2-P1
                up=P3-P2
                down2=P4-P3
                if max([down1,up,down2])-min([down1,up,down2])<2:
                    baseI=Li-3*i2-5
                    baseL=highs[baseI+P1]-lows[baseI+P2]
                    try:
                        baseE=sum(vols[baseI+P1-i2:baseI+P1])
                        if baseE<1:
                            continue
                    except:
                        continue                            
                    features.append([(highs[baseI+P3]-lows[baseI+P2])/baseL,(highs[baseI+P3]-lows[baseI+P4])/baseL,\
                                     sum(vols[baseI+P1+1:baseI+P2+1])/baseE,sum(vols[baseI+P2+1:baseI+P3+1])/baseE,\
                                     sum(vols[baseI+P3+1:baseI+P4+1])/baseE])
                    stocksTarget.append(stocks[i])
                    holds.append(i2)
                    openPrice.append(closes[-1])
                    stopPrice.append(lows[-1])
                    if fig>0:
                        fig-=1
                        plt.figure(figsize=(10,6))
                        ax=plt.subplot()
                        candleData=np.column_stack([range(P4+1),opens[baseI:Li+1],highs[baseI:Li+1],lows[baseI:Li+1],closes[baseI:Li+1]])
                        mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
                        plt.plot([P1,P2,P3,P4],[highs[baseI+P1],lows[baseI+P2],highs[baseI+P3],lows[baseI+P4]],color='k')
                        plt.title(stocks[i])
                        plt.grid()
    if len(stocksTarget)>0:
        stocksTarget=np.array(stocksTarget)
        holds=np.array(holds)
        ModelP=joblib.load('DownUpDownVol')
        prob=ModelP.predict(xgb.DMatrix(data=features))
        tmp=prob>0.5
        probS=prob[tmp]
        stockS=stocksTarget[tmp]
        holdS=holds[tmp]
        openPriceS=np.array(openPrice)[tmp]
        stopPriceS=np.array(stopPrice)[tmp]
        tmp=(-probS).argsort()
        probS=probS[tmp]
        stockS=stockS[tmp]
        holdS=holdS[tmp]
        openPriceS=openPriceS[tmp]
        stopPriceS=stopPriceS[tmp]
        stockTrade=[]
        for i in range(len(stockS)):
            print(stockS[i]+' win ratio:{}% and should be hold {} days'.format(round(probS[i]*100,2),holdS[i]))
            pklData[stockS[i]]=[today.date(),openPriceS[i],holdS[i],stopPriceS[i],probS[i]]
            stockTrade.append(stockS[i])
        tmp=open('X-Scan.pkl','wb')
        pklData['stockTrade']=stockTrade
        pickle.dump(pklData,tmp)
        tmp.close()

    t2=datetime.datetime.now()
    print('Time lapses {} minutes.'.format(round((t2-today).seconds/60,2)))











