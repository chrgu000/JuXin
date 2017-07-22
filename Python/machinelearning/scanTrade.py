# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 08:59:37 2017

@author: caofa
"""
from WindPy import *
import numpy as np
import pickle,datetime,joblib


tradeFlag=raw_input('Please confirm trading or not [y/n]?')
tradeFlag=tradeFlag.lower()=='y'    
w.start()
Tem=w.tlogon('0000', '0', 'W115294100301', '*********', 'SHSZ')
logId=Tem.Data[0][0]
today=datetime.date.today()
try:
    fileTem=open('scanTrade','rb')
    dataTem=pickle.load(fileTem)
    fileTem.close()
    Date=dataTem['Date']
    Opens=dataTem['Opens']
    Closes=dataTem['Closes']
    Highs=dataTem['Highs']
    Lows=dataTem['Lows']
    Vols=dataTem['Vols']
    stocks=dataTem['stocks']
    lastTradeDay=dataTem['lastTradeDay']
    assets=dataTem['assets']
    holdDays=dataTem['holdDays']   
    dateStart=dataTem['dateStart']
    dataTem=w.tquery('Position', 'LogonId='+str(logId))
    holdStocks=dataTem.Data[0]
    holdShares=dataTem.Data[3]
    for i in range(len(holdStocks)):
        try:
            daysi=holdDays[holdStocks[i]]
            if (today-dateStart[holdStocks[i]]).days>=daysi:
                print 'Close %s: %d shares;'%(holdStocks[i],holdShares[i]),
                if tradeFlag:
                    w.torder(holdStocks[i], 'Sell', '0', holdShares[i], 'OrderType=B5TC;'+'LogonID='+str(logId))
                    print 'send trade command!'
                else:
                    print 'not realy trade!'            
        except:
            print 'stocks %s was trade by hand, please close this order by hands too.'%holdStocks[i]      
    dataTem=w.tdays('ED-1TD',today)
    daysTem=dataTem.Data[0]
    if daysTem[1].date()==today:
        lastTradeDay=daysTem[0]
    else:
        lastTradeDay=daysTem[1]
    if Date[-1]<lastTradeDay:
        pickle[-1]# go to except
except:
    dataTem=w.wset('SectorConstituent')
    stocks=dataTem.Data[1]
#    yesterday=today-datetime.timedelta(days=4) # test before; should comment line 77~82,Data.append,Open.append and so on;
    yesterday=today-datetime.timedelta(days=1)
    lastTradeDay=[yesterday]
    assets=[w.tquery('Capital', 'LogonId='+str(logId)).Data[5]]
    holdDays={}    
    dateStart={}
    while 1:
        dataTem=w.wsd(stocks,'open','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F')
        Date=dataTem.Times
        Opens=dataTem.Data
        Closes=w.wsd(stocks,'close','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Highs=w.wsd(stocks,'high','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Lows=w.wsd(stocks,'low','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Vols=w.wsd(stocks,'volume','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        if np.all([len(Opens)-1,len(Closes)-1,len(Highs)-1,len(Lows)-1,len(Vols)-1]):
            dataPKL={'Date':Date,'Opens':Opens,'Closes':Closes,'Highs':Highs,'Lows':Lows,'Vols':Vols}
            break

Date.append(today)
Opens.append(w.wsq(stocks,'rt_open').Data[0])
Closes.append(w.wsq(stocks,'rt_latest').Data[0])
Highs.append(w.wsq(stocks,'rt_high').Data[0])
Lows.append(w.wsq(stocks,'rt_low').Data[0])
Vols.append(w.wsq(stocks,'rt_vol').Data[0])

Lstocks=len(stocks)
stocksi=[] # name of stocks;
handsi=[]  # hands of trading this time;
modeli=[]  # model belonged to;
holdi=[]   # days to hold;
moneyi=[]  # money to trade;
profiti=[] # expected profit of this trading;
indicators=[] 
for i in range(Lstocks):
    Open=Opens[i]
    Close=Closes[i]
    High=Highs[i]
    Low=Lows[i]
    
    Lnan=sum(np.isnan(Open))
    if Lnan>10:
        continue
    else:
        Open=Open[Lnan+1:]
        Close=Close[Lnan+1:]
        Low=Low[Lnan+1:]
        High=High[Lnan+1:]
    if Close[-1]/Close[-2]>=1.095:
        continue
    
    # model 1: spring, model number 1
    hmmSpring=joblib.load('D:\Trading\Python\machinelearning\HMMTem')
    if Close[-2]<Low[-2]+(High[-2]-Low[-2])*0.25 and High[-1]>Low[-1]*1.000001 and 0.025<=Close[-1]/Close[-2]-1<0.055 and Low[-1]/Low[-2]-1>=0.01: 
        flagi=hmmSpring.predict([ np.std([Close[-1],Open[-1],Low[-1],High[-1]])/np.std([Close[-2],Open[-2],Low[-2],High[-2]])-1,\
                                 np.mean(Close[-4:])/np.mean(Close[-11:])-1,High[-1]/High[-2]-1,Close[-1]/Low[-2]-1,Close[-1]/High[-2]-1])
        if flagi==0:
            profiti.append(1.34)
        elif flagi==1:
            profiti.append(3.41)
        elif flagi==3:
            profiti.append(1.44)
        else:
            continue
        stocksi.append(stocks[i])
        handsi.append(np.ceil(100/Close[-1])*100)
        modeli.append(1)   # model number:1;
        holdi.append(2)    # hold 2 days;
        moneyi.append(handsi[-1]*Close[-1])
    
indTem=np.argsort(-np.array(profiti))
profiti=np.array(profiti)[indTem]
stocksi=np.array(stocksi)[indTem]
handsi=np.array(handsi)[indTem]
modeli=np.array(modeli)[indTem]
holdi=np.array(holdi)[indTem]
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
    holdi=holdi[:-Tem]
    moneyi=moneyi[:-Tem]

Ltrade=len(profiti)
for i in range(Ltrade):
    print 'Buy %s: %d shares;use capital:%.f Yuan;profitPerOrder:%.2f,ModelNumber:%d;' %(stocksi[i],handsi[i],moneyi[i],profiti[i],moneyi[i]),
    if tradeFlag:
        w.torder(stocksi[i], 'Buy', '0', handsi[i], 'OrderType=B5TC;'+'LogonID='+str(logId))
        print 'send trade command!'
    else:
        print 'not really trade!'
w.tlogout(str(logId))

holdDaysTem={}
dateStartTem={}
if tradeFlag:
    for i in range(Ltrade):
        holdDaysTem[stocksi[i]]=holdi[i]
        dateStartTem[stocksi[i]]=today
holdDays=dict(holdDays,**holdDaysTem)
dateStart=dict(dateStart,**dateStartTem)
dataPKL['holdDays']=holdDays
dataPKL['dateStart']=dateStart
if lastTradeDay[-1]<today:
    lastTradeDay.append(today)
    assets.append(assetNow)
dataPKL['lastTradeDay']=lastTradeDay
dataPKL['assets']=assets
fileTem=open('scanTrade','wb')
pickle.dump(dataPKL,fileTem)
fileTem.close()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
