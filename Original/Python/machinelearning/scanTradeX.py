# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 08:59:37 2017

@author: caofa
"""

from WindPy import *
import numpy as np
import pandas as pd
import pickle,datetime,time,TrainModel,pdb

t1=time.clock()

TradeDays='30' # how many days to use;
today=datetime.date.today()
yesterday=today-datetime.timedelta(days=1)
Hour=int(time.strftime('%H'))
Minute=int(time.strftime('%M'))
hourMinute=time.strftime('%H-%M')
w.start()
Tem=w.tlogon('0000', '0', 'W115294100301', '*********', 'SHSZ')
logId=Tem.Data[0][0]
tradeFlag=input('Please confirm trading or not(just preparing for trading) or close orders directly [y/n/c]?')
flagInput=tradeFlag.lower()
if flagInput=='c':
    dataTem=w.tquery('Position', 'LogonId='+str(logId))
    for i in range(len(dataTem.Data[0])):
        if dataTem.Data[3][i]>1.0:
             w.torder(dataTem.Data[0][i], 'Sell', '0', dataTem.Data[3][i], 'OrderType=B5TC;'+'LogonID='+str(logId))
             print ('Close %s: %.1f shares;free capital:%.f Yuan;' %(dataTem.Data[0][i],dataTem.Data[3][i],dataTem.Data[3][i]*dataTem.Data[11][i]))            
else:
    tradeFlag=flagInput=='y' 
    tradingDay=len(w.tdays(today,today).Data)>0
    dataTem=w.tquery('Capital', 'LogonId='+str(logId))
    assetNow=dataTem.Data[5]
    try:
        fileTem=open('scanTrade','rb')
        dataPKL=pickle.load(fileTem)
        fileTem.close()
        dateStart=dataPKL['dateStart']
        informTrade=dataPKL['informTrade']
        dateTrade=dataPKL['dateTrade']
        assets=dataPKL['assets']
    except:
        dataPKL={}
        dateStart={}
        assets=[]
        dateTrade=0
        
    if tradeFlag:
        tradeOrNot=0
        profitTable={
                'Spring':{0:1.21,1:1.33,2:2.31,3:1.08,4:0.47},
                'SpringBig':{0:1.25,1:5.00,2:1.05,3:1.75,4:1.24},
                'Up2Down2':{0:1.34,1:3.41,2:2.60,3:-2.81,4:2.34},
                }
        informTrade=pd.DataFrame(informTrade)
        informTradeCopy=informTrade.copy()
        tem=informTrade[1]>0
        informOpen=informTrade.loc[tem,:]
        informClose=informTrade.loc[~tem,:]
        informTrade=informClose
        if dateTrade==today:
            if hourMinute in ['09-29','09-30','09-31']:
                tradingTem=1
            else:
                tem=input('out of good trading opportunity, still close orders [y/n]?')
                tradingTem=tem.lower()=='y'
            if tradingTem:
                tradeOrNo=1
                for i in range(len(informTrade)):
                    w.torder(informTrade.iloc[i,0], 'Sell', '0', -informTrade.iloc[i,1], 'OrderType=B5TC;'+'LogonID='+str(logId))
                    print ('Close %s: %d shares;free capital:%.f Yuan;' %(informTrade.iloc[i,0],-informTrade.iloc[i,1],informTrade.iloc[i,2]))
                    try:
                        dateStart.pop(informTrade.iloc[i,0])
                    except KeyError as e:
                        print(e)
        else:
            print('trading information is not for today, please prepare trading information again and check it!')    
        
        closeTem=np.array(w.wss(informOpen[0].tolist(),'close','tradeDate='+yesterday.strftime('%Y-%m-%d'),'priceAdj=F','cycle=D').Data[0])
        openTem=np.array(w.wsq(informOpen[0].tolist(),'rt_open').Data[0])
        ratioOpen=openTem/closeTem-1    
        for i in range(len(informOpen)):
            if '&' in informOpen.iloc[i,3]:
                tem=informOpen.iloc[i,4]
            else:
                tem=TrainModel.TrainModel(informOpen.iloc[i,3]).kmean.predict(ratioOpen[i])[0]
                tem=profitTable[informOpen.iloc[i,3]][tem]
                if tem>1.5:
                    tem=max(tem,informOpen.iloc[i,4])      
                else:
                    tem=min(tem,informOpen.iloc[i,4])
            informOpen.iloc[i,4]=tem
            if tem>3.0:
                informOpen.iloc[i,1]=informOpen.iloc[i,1]*1
                informOpen.iloc[i,2]=informOpen.iloc[i,2]*1
    #    pdb.set_trace()
        
        informOpen=informOpen.sort_index(by=[4],ascending=False).reset_index(drop=True)   
        informOpen=informOpen.loc[informOpen[4]>1.0]
        moneyCS=informOpen[2].cumsum()
        time.sleep(5)
        dataTem=w.tquery('Capital', 'LogonId='+str(logId))
        availableFun=dataTem.Data[1]
        tem=sum(moneyCS<availableFun)
        informTrade=informOpen.iloc[:tem] 
        if dateTrade==today:
            if hourMinute in ['09-29','09-30','09-31']:
                tradingTem=1
            else:
                tem=input('out of good trading opportunity, still open orders [y/n]?')
                tradingTem=tem.lower()=='y'
            if tradingTem:
                tradeOrNo=1
                for i in range(len(informTrade)):
                    w.torder(informTrade.iloc[i,0], 'Buy', '0', informTrade.iloc[i,1], 'OrderType=B5TC;'+'LogonID='+str(logId))
                    print ('Buy %s: %d shares;use capital:%.f Yuan;Model:%s;profitPerOrder:%.2f;' \
                           %(informTrade.iloc[i,0],informTrade.iloc[i,1],informTrade.iloc[i,2],informTrade.iloc[i,3],informTrade.iloc[i,4]))
        else:
            print('trading information is not for today, please prepare trading information again and check it!')
        
        if tradeOrNot:
            dataPKL['dateStart']=dateStart
            dataPKL['assets']=assets
            dataPKL['informTrade']=informTradeCopy
            dataPKL['dateTrade']=0
            fileTem=open('scanTrade','wb')
            pickle.dump(dataPKL,fileTem)
            fileTem.close()
            
    else:
        informTrade=[]
        if Hour*100+Minute>=930:
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
        
        dataTem=w.tquery('Position', 'LogonId='+str(logId))
        if len(dataTem.Data)>3:
            sharesHold=np.array(dataTem.Data[7]);
            tem=sharesHold>0;sharesHold=sharesHold[tem];
            priceHold=np.array(dataTem.Data[11])[tem];stocksHold=np.array(dataTem.Data[0])[tem]
            Lt=len(stocksHold)
            if Lt>0:
                fileTem=open('scanTrade','rb')
                dataPKL=pickle.load(fileTem)
                fileTem.close()
                dateStart=dataPKL['dateStart']
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
    #        print(i,end=',')        
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
            
    #        if stocks[i]=='300029.SZ':
    #            pdb.set_trace()
                
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
                     (highs[i2]-lows[i2])/(highs[i2-1]-lows[i2-1]),\
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
                    flagNot=[[1, [2]], [15, [3, 4]]]
                    flagOk=[[1, [0, 1, 3, 4]], [15, [0, 1, 2]]]
                    ReSelectNot=TM.kmeanTestCertainNot([Matrix],flagNot)      # value 0 or 1      
                    ReSelectOk=TM.kmeanTestCertainOk([Matrix],flagOk)        # value 0 or 1 or 2 or 2+
                    if ReSelectNot*ReSelectOk:
                        flag=TM.xgbPredict(np.array([Matrix])) # should np.array([Matrix]) or there is something wrong;
                        if flag[0]==1:
                            if stocks[i][0]=='0':
                                ratioTem=1.030
                            elif stocks[i][0]=='3':
                                ratioTem=1.197
                            else:
                                ratioTem=0.915                 
                            if wd=='3':
                                profiti2.append(2.32*ratioTem)
                            elif wd=='5':
                                profiti2.append(2.23*ratioTem)
                            elif wd=='4':
                                profiti2.append(1.90*ratioTem)
                            elif wd=='2':
                                profiti2.append(1.85*ratioTem)
                            if wd!='1':
                                stocksi2.append(stocks[i])
                                handsi2.append(np.ceil(100/closes[-1])*100)
                                modeli2.append(modelTem)   # model number:1;
                                moneyi2.append(handsi2[-1]*closes[-1])
               
                modelTem='Spring'
                if modelTem in modelSelect: # model 1: Up2Down2, model number 1
                    TM=TrainModel.TrainModel(modelTem)
                    flagNot=[[1, [1, 2, 4]], [6, [2, 3, 4]]]
                    flagOk= [[1, [0, 3]], [6, [1]]]
                    ReSelectNot=TM.kmeanTestCertainNot([Matrix],flagNot)      # value 0 or 1      
                    ReSelectOk=TM.kmeanTestCertainOk([Matrix],flagOk)        # value 0 or 1 or 2 or 2+
                    if ReSelectNot*ReSelectOk:
                        flag=TM.xgbPredict(np.array([Matrix])) # should np.array([Matrix]) or there is something wrong;
                        if flag[0]==1:
                            if stocks[i][0]=='0':
                                ratioTem=1.012
                            elif stocks[i][0]=='3':
                                ratioTem=1.089
                            else:
                                ratioTem=0.963                         
                            if wd=='1':
                                profiti2.append(1.67*ratioTem)
                            elif wd=='5':
                                profiti2.append(1.33*ratioTem)
                            elif wd=='2':
                                profiti2.append(1.27*ratioTem)
                            
                            if wd not in ['3','4']:
                                stocksi2.append(stocks[i])
                                handsi2.append(np.ceil(100/closes[-1])*100)
                                modeli2.append(modelTem)   # model number:1;
                                moneyi2.append(handsi2[-1]*closes[-1])
                modelTem='SpringBig'
                if modelTem in modelSelect: # model 1: Up2Down2, model number 1
                    TM=TrainModel.TrainModel(modelTem)
                    flagNot=[[4, [4]], [5, [2, 3]], [12, [3]], [14, [0]], [21, [0]]]
                    flagOk= [[0, [3]], [5, [4]], [10, [1, 3]], [14, [1, 4]], [20, [4]], [21, [3, 4]], [23, [2]], [27, [1, 3]]]
                    ReSelectNot=TM.kmeanTestCertainNot([Matrix],flagNot)      # value 0 or 1      
                    ReSelectOk=TM.kmeanTestCertainOk([Matrix],flagOk)        # value 0 or 1 or 2 or 2+
                    if ReSelectNot*ReSelectOk:
                        flag=TM.xgbPredict(np.array([Matrix])) # should np.array([Matrix]) or there is something wrong;
                        if flag[0]==1:
                            if stocks[i][0]=='0':
                                ratioTem=1.079
                            elif stocks[i][0]=='3':
                                ratioTem=0.764
                            else:
                                ratioTem=0.984
                            if wd=='1':
                                profiti2.append(2.55*ratioTem)
                            elif wd=='2':
                                profiti2.append(1.93*ratioTem)
                            elif wd=='3':
                                profiti2.append(1.56*ratioTem)
                            elif wd=='5':
                                profiti2.append(1.32*ratioTem)
                            if wd!='4':
                                stocksi2.append(stocks[i])
                                handsi2.append(np.ceil(100/closes[-1])*100)
                                modeli2.append(modelTem)   # model number:1;
                                moneyi2.append(handsi2[-1]*closes[-1])
                                
                if 'test' in modelSelect: 
                    pass
                
                lenSelect=len(profiti2)
                if lenSelect>0:
                    stocksi.append(stocksi2[0])
                    handsi.append(handsi2[0])
                    moneyi.append(moneyi2[0]) 
                    modeli.append('&'.join(modeli2))
                    if lenSelect==1:
                        profiti.append(profiti2[0])    
                    else:
                        profiti.append(max(profiti2)*1.5)     
        
        if tradingDay:
            if Hour<15:
                dateFor=today
            else:
                dateFor=w.tdays(today,today+timedelta(days=12)).Data[0][1].date()
        else:
            dateFor=w.tdays(today,today+timedelta(days=12)).Data[0][0].date()
    
        if dateTrade!=dateFor:
            assets.append(assetNow)
            
        dataPKL['assets']=assets
        dataPKL['dateTrade']=dateFor
        
        tem=np.argsort(profiti)[::-1]
        profiti=np.array(profiti)[tem]
        stocksi=np.array(stocksi)[tem]
        handsi=np.array(handsi)[tem]
        moneyi=np.array(moneyi)[tem]
        modeli=np.array(modeli)[tem]
        
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
        
        print('')
        for i in range(len(informTrade)):
            informi=informTrade[i]
            if informi[1]>0:
                print('Buy %s %d shares, occupy money %.1f; Model %s, Expect %.2f%%.' %(informi[0],informi[1],informi[2],informi[3],informi[4]))        
            else:
                print('Close %s %d shares, free money %.1f. ' %(informi[0],informi[1],informi[2]))

t2=time.clock()
print('time elapses:%.1f minute' %((t2-t1)/60))
        
        
        
        
        
        
        
