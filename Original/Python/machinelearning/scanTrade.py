# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 08:59:37 2017

@author: caofa
"""
from WindPy import *
import numpy as np
import pickle,datetime,time,TrainModel

t1=time.clock()
firstTime=0 # control whether this is the first time to run this procedure;


TradeDays='30' # how many days to use;
Reload=1 # re-down load data;
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
    dataPKL=pickle.load(fileTem)
    fileTem.close()
    stocks=dataPKL['stocks']    
    Opens=dataPKL['Opens']
    Closes=dataPKL['Closes']
    Highs=dataPKL['Highs']
    Lows=dataPKL['Lows']
    Vols=dataPKL['Vols']
    assets=dataPKL['assets']
    holdDays=dataPKL['holdDays']   
    dateStart=dataPKL['dateStart']
    if dataPKL['date_update']==time.strftime('%Y-%m-%d'):
        Reload=0
    dataTem=w.tquery('Position', 'LogonId='+str(logId))
    if len(dataTem.Data)>3:
        holdStocks=dataTem.Data[0]
        holdShares=dataTem.Data[3]   
        holdOrders=1  
if firstTime or Reload:
    dataTem=w.wset('SectorConstituent')
    stocks=dataTem.Data[1]
    assets=[w.tquery('Capital', 'LogonId='+str(logId)).Data[5]]
    while 1:
        Opens=w.wsd(stocks,'open','ED-'+TradeDays+'TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Closes=w.wsd(stocks,'close','ED-'+TradeDays+'TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Highs=w.wsd(stocks,'high','ED-'+TradeDays+'TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Lows=w.wsd(stocks,'low','ED-'+TradeDays+'TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Vols=w.wsd(stocks,'volume','ED-'+TradeDays+'TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        if np.all([len(Opens)-1,len(Closes)-1,len(Highs)-1,len(Lows)-1,len(Vols)-1]):
            break
    if firstTime:
        holdDays={}    
        dateStart={}
        dataPKL={'Opens':Opens,'Closes':Closes,'Highs':Highs,'Lows':Lows,'Vols':Vols,'stocks':stocks}
    else:
        dataPKL['Opens']=Opens;dataPKL['Closes']=Closes;dataPKL['Highs']=Highs;dataPKL['Lows']=Lows;dataPKL['Vols']=Vols;dataPKL['stocks']=stocks;

Opens=np.column_stack([np.row_stack(Opens),w.wsq(stocks,'rt_open').Data[0]])
Closes=np.column_stack([np.row_stack(Closes),w.wsq(stocks,'rt_latest').Data[0]])
Highs=np.column_stack([np.row_stack(Highs),w.wsq(stocks,'rt_high').Data[0]])
Lows=np.column_stack([np.row_stack(Lows),w.wsq(stocks,'rt_low').Data[0]])
Vols=np.column_stack([np.row_stack(Vols),w.wsq(stocks,'rt_vol').Data[0]])        
        
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
    opens=Opens[i]
    closes=Closes[i]
    highs=Highs[i]
    lows=Lows[i]
    vols=Vols[i]
    
    Lnan=sum(np.isnan(opens))
    if Lnan>5:
        continue
    else:
        opens=opens[Lnan+1:]
        closes=closes[Lnan+1:]
        lows=lows[Lnan+1:]
        highs=highs[Lnan+1:]
        vols=vols[Lnan+1:]        
    if closes[-1]/closes[-2]>=1.095:
        continue
    i2=len(opens)-1
    
    modelSelect=[]
    if lows[i2-3]<=min(lows[i2-5:i2+1]) and highs[i2-2]>highs[i2-3] and highs[i2-1]>highs[i2] and lows[i2-1]>lows[i2] and \
            highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2]: #model 1
                modelSelect.append(1)
    if 0: #model2
        pass
    
    if len(modelSelect)>0:
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
             vols[i2]/vols[i2-3] ]     
        
        profiti2=[]# for one stocks fits more than 1 stock
        stocksi2=[]
        handsi2=[]
        modeli2=[]
        holdi2=[]
        moneyi2=[]
        
        if 1 in modelSelect: # model 1: Up2Down2, model number 1
            TM=TrainModel.TrainModel('Up2Down2')
            flagNot=[[0, [0, 2]], [1, [1, 4]], [2, [2]], [6, [1, 3]]]
            flagOk=[[0, [1, 4]], [1, [0, 3]], [2, [1, 3, 4]], [3, [0, 3]], [4, [3]], [6, [2, 4]]]
            tem=np.ones(len(Matrix)).tolist()
            ReSelectNot=TM.hmmTestCertainNot([tem,Matrix],flagNot)      # value 0 or 1      
            ReSelectOk=TM.hmmTestCertainOk([tem,Matrix],flagOk)        # value 0 or 1 or 2 or 2+
            print(ReSelectNot)
            print(ReSelectOk)
            print(TM.xgbPredict(np.array([Matrix])))
            print('-'*100)
            if ReSelectNot[-1]*ReSelectOk[-1]:
                flag=TM.xgbPredict(np.array([Matrix])) # should np.array([Matrix]) or there is something wrong;
                if flag[0]==2:
                    profiti2.append(2.7)
                else:
                    continue
                stocksi2.append(stocks[i])
                handsi2.append(np.ceil(100/closes[-1])*100)
                modeli2.append('Up2Down2')   # model number:1;
                holdi2.append(2)    # hold 2 days unless close[today]<close[yesterday]
                moneyi2.append(handsi[-1]*closes[-1])
        if 2 in modelSelect: # model 1: xxxxx, model number 2
            pass
        
        if len(profiti2)>1:
            tem=np.argsort(profiti2)
            profiti.append(profiti2[tem]*1.5)
            stocksi.append(stocksi2[tem])
            handsi.append(handsi2[tem]*2)
            modeli.append('&'.join(modeli2))
            holdi.append(holdi2[tem])
            moneyi.append(moneyi2[tem]*2)            

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
    print ('Buy %s: %d shares;use capital:%.f Yuan;profitPerOrder:%.2f,Model:%s;' %(stocksi[i],handsi[i],moneyi[i],profiti[i],modeli[i]),)
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
dataPKL['date_update']=time.strftime('%Y-%m-%d')
fileTem=open('scanTrade','wb')
pickle.dump(dataPKL,fileTem)
fileTem.close()

t2=time.clock()
print('time elapses:%.1f minute' %((t2-t1)/60))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
