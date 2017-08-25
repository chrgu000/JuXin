# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 08:59:37 2017

@author: caofa
"""
from WindPy import *
import numpy as np
import pickle,datetime,joblib,time

t1=time.clock()
firstTime=1 # control whether this is the first time to run this procedure;
Reload=0 # re-down load data;
holdOrders=0 # record wether hold orders;
tradeFlag=input('Please confirm trading or not [y/n]?')
tradeFlag=tradeFlag.lower()=='y'    
w.start()
Tem=w.tlogon('0000', '0', 'W115294100301', '*********', 'SHSZ')
logId=Tem.Data[0][0]
today=datetime.date.today()
yesterday=today-datetime.timedelta(days=1)

if not firstTime:
    fileTem=open('scanTrade','rb')
    dataTem=pickle.load(fileTem)
    fileTem.close()
    Date=dataTem['Date']
    stocks=dataTem['stocks']    
    Opens=dataTem['Opens']
    Closes=dataTem['Closes']
    Highs=dataTem['Highs']
    Lows=dataTem['Lows']
    Vols=dataTem['Vols']
    assets=dataTem['assets']
    holdDays=dataTem['holdDays']   
    dateStart=dataTem['dateStart']
    dataTem=w.tquery('Position', 'LogonId='+str(logId))
    if len(dataTem.Data)>3:
        holdStocks=dataTem.Data[0]
        holdShares=dataTem.Data[3]   
        holdOrders=1    
    lastTradeDay=w.tdays('ED-1TD',today).Data[0][0]
    if lastTradeDay==Date[-1]:
        Opens=np.column_stack([np.row_stack(Opens),w.wsq(stocks,'rt_open').Data[0]])
        Closes=np.column_stack([np.row_stack(Closes),w.wsq(stocks,'rt_latest').Data[0]])
        Highs=np.column_stack([np.row_stack(Highs),w.wsq(stocks,'rt_high').Data[0]])
        Lows=np.column_stack([np.row_stack(Lows),w.wsq(stocks,'rt_low').Data[0]])
        Vols=np.column_stack([np.row_stack(Vols),w.wsq(stocks,'rt_vol').Data[0]])        
    else:
        Reload=1
if firstTime or Reload:
    dataTem=w.wset('SectorConstituent')
    stocks=dataTem.Data[1]
    assets=[w.tquery('Capital', 'LogonId='+str(logId)).Data[5]]
    if firstTime:
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
            dataPKL={'Date':Date,'Opens':Opens,'Closes':Closes,'Highs':Highs,'Lows':Lows,'Vols':Vols,'stocks':stocks}
            Opens=np.column_stack([np.row_stack(Opens),w.wsq(stocks,'rt_open').Data[0]])
            Closes=np.column_stack([np.row_stack(Closes),w.wsq(stocks,'rt_latest').Data[0]])
            Highs=np.column_stack([np.row_stack(Highs),w.wsq(stocks,'rt_high').Data[0]])
            Lows=np.column_stack([np.row_stack(Lows),w.wsq(stocks,'rt_low').Data[0]])
            Vols=np.column_stack([np.row_stack(Vols),w.wsq(stocks,'rt_vol').Data[0]])
            break
        
if holdOrders: # close orders or not
    for i in range(len(holdStocks)):
        try:
            daysi=holdDays[holdStocks[i]]
            closeTem=Closes[stocks.index(holdStocks[i])]
            tem=len(w.tdays(dateStart[holdStocks[i]],today).Data[0])
            if tem>=daysi+1 or (tem==2 and closeTem[-1]<closeTem[-2]):
                print('Close %s: %d shares;'%(holdStocks[i],holdShares[i]),)
                if tradeFlag:
                    w.torder(holdStocks[i], 'Sell', '0', holdShares[i], 'OrderType=B5TC;'+'LogonID='+str(logId))
                    holdDays.pop(holdStocks[i])
                    print( 'send trade command!')
                else:
                    print ('not realy trade!')       
        except:
            print ('stocks %s was trade by hand, please close this order by hands too.'%holdStocks[i])
        
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
    hmmSpring=joblib.load('D:\Trade\Python\machinelearning\modelTestSpringHMM') 
    if Close[-2]<Low[-2]+(High[-2]-Low[-2])*0.25 and High[-1]>Low[-1]*1.000001 and 0.025<=Close[-1]/Close[-2]-1<0.055 and Low[-1]/Low[-2]-1>=0.01: 
        flagi=hmmSpring.predict([ np.std([Close[-1],Open[-1],Low[-1],High[-1]])/np.std([Close[-2],Open[-2],Low[-2],High[-2]]),\
                                 np.mean(Close[-4:])/np.mean(Close[-11:]),High[-1]/High[-2],Close[-1]/Low[-2],Close[-1]/High[-2]  ])
        if flagi==0:
            profiti.append(1.7)
        elif flagi==2:
            profiti.append(3.7)
        elif flagi==4:
            profiti.append(1.6)
        else:
            continue
        stocksi.append(stocks[i])
        handsi.append(np.ceil(100/Close[-1])*100)
        modeli.append(1)   # model number:1;
        holdi.append(2)    # hold 2 days unless close[today]<close[yesterday]
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
    print ('Buy %s: %d shares;use capital:%.f Yuan;profitPerOrder:%.2f,ModelNumber:%d;' %(stocksi[i],handsi[i],moneyi[i],profiti[i],moneyi[i]),)
    if tradeFlag:
        w.torder(stocksi[i], 'Buy', '0', handsi[i], 'OrderType=B5TC;'+'LogonID='+str(logId))
        print('send trade command!')
    else:
        print ('not really trade!')
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
dataPKL['assets']=assets
fileTem=open('scanTrade','wb')
pickle.dump(dataPKL,fileTem)
fileTem.close()

t2=time.clock()
print('time elapses:%.1f minute' %((t2-t1)/60))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
