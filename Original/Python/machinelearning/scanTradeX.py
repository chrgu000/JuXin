# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 08:59:37 2017

@author: caofa
"""
from WindPy import *
import numpy as np
import pandas as pd
import pickle,datetime,time,TrainModel

t1=time.clock()

TradeDays='30' # how many days to use;
today=datetime.date.today()
yesterday=today-datetime.timedelta(days=1)
Hour=int(time.strftime('%H'))
hourMinute=time.strftime('%H-%M')
tradeFlag=input('Please confirm trading or not(just preparing for trading) [y/n]?')
tradeFlag=tradeFlag.lower()=='y' 
w.start()
Tem=w.tlogon('0000', '0', 'W115294100301', '*********', 'SHSZ')
logId=Tem.Data[0][0]
tradingDay=len(w.tdays(today,today).Data[0])>0
try:
    fileTem=open('scanTrade','rb')
    dataPKL=pickle.load(fileTem)
    fileTem.close()
    dateStart=dataPKL['dateStart']
    informTrade=dataPKL['informTrade']
    dateTrade=dataPKL['dateTrade']
except:
    dataPKL={}
    dateStart={}
    
if tradeFlag:
    if dateTrade==today:
        if hourMinute in ['09-30','09-31']:
            tradingTem=1
        else:
            tem=input('out of good trading opportunity, still trade [y/n]?')
            tradingTem=tem.lower()=='y'
        if tradingTem:
            for i in range(len(informTrade)):
                if informTrade[i][1]>0:
                    w.torder(informTrade[i][0], 'Buy', '0', informTrade[i][1], 'OrderType=B5TC;'+'LogonID='+str(logId))
                    print ('Buy %s: %d shares;use capital:%.f Yuan;Model:%s;profitPerOrder:%.2f;' \
                           %(informTrade[i][0],informTrade[i][1],informTrade[i][2],informTrade[i][3],informTrade[i][4]))
                else:
                    w.torder(informTrade[i][0], 'Sell', '0', -informTrade[i][1], 'OrderType=B5TC;'+'LogonID='+str(logId))
                    print ('Close %s: %d shares;use capital:%.f Yuan;Model:%s;profitPerOrder:%.2f;' \
                           %(informTrade[i][0],-informTrade[i][1],informTrade[i][2],informTrade[i][3],informTrade[i][4]))
                    try:
                        dateStart.pop(informTrade[i][0])
                    except KeyError as e:
                        print(e)
                            
            dataPKL['dateStart']=dateStart
            dataPKL['informTrade']=informTrade
            dataPKL['dateTrade']=0
            fileTem=open('scanTrade','wb')
            pickle.dump(dataPKL,fileTem)
            fileTem.close()
    else:
        print('trading information is not for today, please prepare trading information again and check it!')
        
else:
    informTrade=[]
    if Hour>=15:
        dateEnd=today
    else:
        dateEnd=yesterday
    dataTem=w.wset('SectorConstituent')
    stocks=dataTem.Data[1]
    Opens=w.wsd(stocks,'open','ED-'+TradeDays+'TD',dateEnd,'Fill=Previous','PriceAdj=F').Data
    Closes=w.wsd(stocks,'close','ED-'+TradeDays+'TD',dateEnd,'Fill=Previous','PriceAdj=F').Data
    Highs=w.wsd(stocks,'high','ED-'+TradeDays+'TD',dateEnd,'Fill=Previous','PriceAdj=F').Data
    Lows=w.wsd(stocks,'low','ED-'+TradeDays+'TD',dateEnd,'Fill=Previous','PriceAdj=F').Data
    Vols=w.wsd(stocks,'volume','ED-'+TradeDays+'TD',dateEnd,'Fill=Previous','PriceAdj=F').Data
    
    tem=w.tquery('Position', 'LogonId='+str(logId))
    stocksHold=tem.Data[0];sharesHold=tem.Data[3];priceHold=tem.Data[11]
    Lt=len(stocksHold)
    if Lt>0:
        fileTem=open('scanTrade','rb')
        dataPKL=pickle.load(fileTem)
        fileTem.close()
        dateStart=dataPKL['dateStart']
        informTrade=[]
        for i in range(Lt):
            datei=dateStart[stocksHold[i]]
            indi=stocks.index(stocksHold[i])
            if len(w.tdays(datei,dateEnd).Data[0])>=2 or Closes[indi][-1]<Closes[indi][-2]:
                informTrade.append([stocksHold[i],-sharesHold[i],priceHold[i]*sharesHold[i],'close',10])
    
    Lstocks=len(stocks)
    stocksi=[] # name of stocks;
    handsi=[]  # hands of trading this time;
    modeli=[]  # model belonged to;
    moneyi=[]  # money to trade;
    profiti=[] # expected profit of this trading;
    indicators=[] 
    for i in range(Lstocks):
        opens=Opens[i]
        closes=Closes[i]
        highs=Highs[i]
        lows=Lows[i]
        vols=Vols[i]
        
        Lnan=sum(np.isnan(opens))
        if Lnan>5:
            continue
        else:
            opens=np.array(opens[Lnan+1:])
            closes=np.array(closes[Lnan+1:])
            lows=np.array(lows[Lnan+1:])
            highs=np.array(highs[Lnan+1:])
            vols=np.array(vols[Lnan+1:])
        if closes[-1]/closes[-2]>=1.095:
            continue
        i2=len(opens)-1        
        modelSelect=[]
        if lows[i2-3]<=min(lows[i2-5:i2+1]) and highs[i2-2]>highs[i2-3] and highs[i2-1]>highs[i2] and lows[i2-1]>lows[i2] and \
        highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2]:
            modelSelect.append('Up2Down2')
        if closes[i2-1]<lows[i2-1]+(highs[i2-1]-lows[i2-1])/4  and closes[i2]>lows[i2]+(highs[i2]-lows[i2])*3/4  and \
        highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2]:
            modelSelect.append('Spring')
        if closes[i2-1]<lows[i2-2] and closes[i2]>highs[i2-1] and closes[i2-1]>=lows[i2-1]+(highs[i2-1]-lows[i2-1])/4 and\
        highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2]: #vols[i2-2:i
             modelSelect.append('SpringBig')
             
        if 0: #next model
            pass
        
        if len(modelSelect)>0:
            if tradingDay:
                if Hour>=15:
                    wd=w.tdays(today,today+timedelta(days=10)).Data[0][1].strftime('%w')
                else:
                    wd=today.strftime('%w')
            else:
                wd=w.tdays(today,today+timedelta(days=10)).Data[0][0].strftime('%w')                    
            max5near=max(closes[i2-4:i2+1]);max5far=max(closes[i2-9:i2-4]);
            min5near=min(closes[i2-4:i2+1]);min5far=min(closes[i2-9:i2-4]);
            max_7near=max(highs[i2-6:i2+1]);max_7far=max(highs[i2-13:i2-6]);
            min_7near=min(lows[i2-6:i2+1]);min_7far=min(lows[i2-13:i2-6]);
            if max_7near>max_7far and min_7near>min_7far:
                ud_7=1
            elif max_7near<max_7far and min_7near<min_7far:
                ud_7=-1
            else:
                ud_7=0                                                       
            Matrix=[ opens[i2]/highs[i2-1],\
                 lows[i2]/highs[i2-1],\
                 min5near/min5far,\
                 closes[i2-4:i2].mean()/closes[i2-9:i2].mean(),\
                 max5near/max5far,\
                 highs[i2-4:i2].mean()/highs[i2-9:i2].mean(),\
                 lows[i2]/opens[i2-1],\
                 highs[i2]/highs[i2-1],\
                 lows[i2]/lows[i2-1],\
                 lows[i2]/closes[i2-1],\
                 (vols[i2]+vols[i2-1])/(vols[i2-3]+vols[i2-2]),\
                 vols[i2-1]/vols[i2-2],\
                 vols[i2]/vols[i2-2],\
                 closes[i2-4:i2].std()/closes[i2-9:i2].std(),\
                 highs[i2]/closes[i2-1],\
                 ud_7,\
                 opens[i2]/closes[i2-1],\
                 vols[i2-1]/vols[i2-3],\
                 highs[i2]/lows[i2-1],\
                 vols[i2]/vols[i2-3],\
                 closes[i2]/np.mean(opens[i2-4:i2]),\
                 pd.DataFrame([lows[i2-3],opens[i2-3],closes[i2-3],highs[i2-3]])[0].corr(pd.DataFrame([lows[i2],closes[i2],opens[i2],highs[i2]])[0]),\
                 vols[i2]/vols[i2-1],\
                 highs[i2-4:i2].std()/highs[i2-9:i2].std(),\
                 vols[i2-2]/vols[i2-3],\
                 np.std([ closes[i2],opens[i2],highs[i2],lows[i2] ])/np.std([closes[i2-1],opens[i2-1],highs[i2-1],lows[i2-1]]),\
                 closes[i2]/closes[i2-1],\
                 opens[i2]/lows[i2-1],\
                 highs[i2]/opens[i2-1] ]      
            
            profiti2=[]# for one stocks fits more than 1 stock
            stocksi2=[]
            handsi2=[]
            modeli2=[]
            moneyi2=[]
            
            modelTem='Up2Down2'
            if modelTem in modelSelect: # model 1: Up2Down2, model number 1
                TM=TrainModel.TrainModel(modelTem)
                flagNot=[[1, [1]], [15, [3, 4]]]
                flagOk=[[1, [0, 2, 3, 4]], [15, [0, 1, 2]]]
                tem=np.ones(len(Matrix)).tolist()
                ReSelectNot=TM.kmeanTestCertainNot([tem,Matrix],flagNot)      # value 0 or 1      
                ReSelectOk=TM.kmeanTestCertainOk([tem,Matrix],flagOk)        # value 0 or 1 or 2 or 2+
                if ReSelectNot[-1]*ReSelectOk[-1]:
                    flag=TM.xgbPredict(np.array([Matrix])) # should np.array([Matrix]) or there is something wrong;
                    if flag[0]==1:
                        if wd=='5':
                            profiti2.append(2.42)
                        elif wd=='3':
                            profiti2.append(2.24)
                        elif wd=='2':
                            profiti2.append(1.82)
                        elif wd=='4':
                            profiti2.append(1.61)
                        if wd!='1':
                            stocksi2.append(stocks[i])
                            handsi2.append(np.ceil(100/closes[-1])*100)
                            modeli2.append(modelTem)   # model number:1;
                            moneyi2.append(handsi2[-1]*closes[-1])
            modelTem='Spring'
            if modelTem in modelSelect: # model 1: Up2Down2, model number 1
                TM=TrainModel.TrainModel(modelTem)
                flagNot=[[1, [1, 3, 4]], [6, [0, 1, 4]]]
                flagOk= [[1, [0]], [6, [3]]]
                tem=np.ones(len(Matrix)).tolist()
                ReSelectNot=TM.kmeanTestCertainNot([tem,Matrix],flagNot)      # value 0 or 1      
                ReSelectOk=TM.kmeanTestCertainOk([tem,Matrix],flagOk)        # value 0 or 1 or 2 or 2+
                if ReSelectNot[-1]*ReSelectOk[-1]:
                    flag=TM.xgbPredict(np.array([Matrix])) # should np.array([Matrix]) or there is something wrong;
                    if flag[0]==1:
                        if wd=='1':
                            profiti2.append(1.76)
                        elif wd=='5':
                            profiti2.append(1.28)
                        elif wd=='2':
                            profiti2.append(1.19)
                        elif wd=='3':
                            profiti2.append(1.1)
                        if wd!='4':
                            stocksi2.append(stocks[i])
                            handsi2.append(np.ceil(100/closes[-1])*100)
                            modeli2.append(modelTem)   # model number:1;
                            moneyi2.append(handsi2[-1]*closes[-1])
            modelTem='SpringBig'
            if modelTem in modelSelect: # model 1: Up2Down2, model number 1
                TM=TrainModel.TrainModel(modelTem)
                flagNot=[[3, [3, 4]], [4, [2]], [5, [2]], [19, [4]], [20, [4]]]
                flagOk= [[3, [0]], [5, [0, 4]], [10, [3]], [19, [0, 1, 3]], [20, [0, 3]]]
                tem=np.ones(len(Matrix)).tolist()
                ReSelectNot=TM.kmeanTestCertainNot([tem,Matrix],flagNot)      # value 0 or 1      
                ReSelectOk=TM.kmeanTestCertainOk([tem,Matrix],flagOk)        # value 0 or 1 or 2 or 2+
                if ReSelectNot[-1]*ReSelectOk[-1]:
                    flag=TM.xgbPredict(np.array([Matrix])) # should np.array([Matrix]) or there is something wrong;
                    if flag[0]==1:
                        if wd=='1':
                            profiti2.append(1.85)
                        elif wd=='2':
                            profiti2.append(1.82)
                        elif wd=='5':
                            profiti2.append(1.62)
                        elif wd=='3':
                            profiti2.append(1.2)
                        if wd!='4':
                            stocksi2.append(stocks[i])
                            handsi2.append(np.ceil(100/closes[-1])*100)
                            modeli2.append(modelTem)   # model number:1;
                            moneyi2.append(handsi2[-1]*closes[-1])
                            
            if 'test' in modelSelect: 
                pass
            
            lenSelect=len(profiti2)
            if lenSelect==1:
                profiti.append(profiti2[0])
                stocksi.append(stocksi2[0])
                handsi.append(handsi2[0])
                modeli.append('&'.join(modeli2))
                moneyi.append(moneyi2[0]) 
            elif lenSelect>1:
                profiti.append(max(profiti2)*1.5)
                if profiti[-1]>3.0:
                    mult=2
                else:
                    mult=1
                stocksi.append(stocksi2[0])
                handsi.append(handsi2[0]*mult)
                modeli.append('&'.join(modeli2))
                moneyi.append(moneyi2[0]*mult)             
    
    indTem=np.argsort(-np.array(profiti))
    profiti=np.array(profiti)[indTem]
    stocksi=np.array(stocksi)[indTem]
    handsi=np.array(handsi)[indTem]
    modeli=np.array(modeli)[indTem]
    moneyi=np.array(moneyi)[indTem]
    dataTem=w.tquery('Capital', 'LogonId='+str(logId))
    availableFun=dataTem.Data[1]
    assetNow=dataTem.Data[5]
    moneyCS=np.cumsum(moneyi)
    Tem=sum(moneyCS>availableFun)
    if Tem>0:
        profiti=profiti[:-Tem]
        stocksi=stocksi[:-Tem]
        handsi=handsi[:-Tem]
        modeli=modeli[:-Tem]
        moneyi=moneyi[:-Tem]
    
    if tradingDay:
        if Hour<15:
            dateFor=today
        else:
            dateFor=w.tdays(today,today+timedelta(days=12)).Data[0][1].date()
    else:
        dateFor=w.tdays(today,today+timedelta(days=12)).Data[0][0].date()
    dataPKL['dateTrade']=dateFor
    
    Ltrade=len(profiti)
    dateStarti={}
    for i in range(Ltrade):
        informTrade.append([stocksi[i],handsi[i],moneyi[i],modeli[i],profiti[i]])
        dateStarti[stocksi[i]]=dateFor
    w.tlogout(str(logId))
    dateStart=dict(dateStart,**dateStarti)
    dataPKL['dateStart']=dateStart
    dataPKL['informTrade']=informTrade    
        
    fileTem=open('scanTrade','wb')
    pickle.dump(dataPKL,fileTem)
    fileTem.close()
    
    for i in range(len(informTrade)):
        informi=informTrade[i]
        if informi[1]>0:
            print('Buy %s %d shares, occupy money %.1f; Model %s, Expect %.2f%%.' %(informi[0],informi[1],informi[2],informi[3],informi[4]))        
        else:
            print('Close %s %d shares, free money %.1f. ' %(informi[0],informi[1],informi[2]))

t2=time.clock()
print('time elapses:%.1f minute' %((t2-t1)/60))
        
        
        
        
        
        
        
