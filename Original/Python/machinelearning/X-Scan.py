## -*- coding: utf-8 -*-
#"""
#Created on Wed Apr 11 17:15:20 2018
#
#@author: Administrator
#"""
#import tushare as ts
#import numpy as np
#import xgboost as xgb
#import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
#import datetime,pickle,pdb,joblib
#
#today=datetime.datetime.today()
##if 1: # only for the first time run
##    tmp=open('X-Scan.pkl','wb')
##    pklData={'dateSave':(today-datetime.timedelta(5)).date(),'profits':[],'stockTrade':[]}
##    pickle.dump(pklData,tmp)
##    tmp.close()    
#tradeTime=14<=today.hour<15 and today.minute>50
#tmp=open('X-Scan.pkl','rb')
#pklData=pickle.load(tmp)
#tmp.close()
#fig=0
#if (today.date()-pklData['dateSave']).days>0:
#    tmp=ts.get_stock_basics()
#    stocks=tmp.index
#    L=len(stocks)
#    nDays=50 #number of natural days;
#    dataCall=[]
#    for i in range(L):
#        tmp=ts.get_k_data(code = stocks[i],start = datetime.datetime.strftime(today-datetime.timedelta(nDays),'%Y-%m-%d'))
#        dataCall.append(tmp)
#    #print('time lapse {} minutes.'.format(round((t2-today).seconds/60,2)))
#    pklData['dateSave']=today.date()
#    pklData['dataCall']=dataCall
#    pklData['stocks']=stocks
#    tmp=open('X-Scan.pkl','wb')
#    pickle.dump(pklData,tmp)
#    tmp.close()
#    t2=datetime.datetime.now()
#    print('Updating data has been completed now! and time lapses {} minutes.'.format(round((t2-today).seconds/60,2)))
#else:
#    stocks=pklData['stocks'].tolist()
#    stockTrade=pklData['stockTrade'].copy()
#    dataCall=pklData['dataCall']
#
#    dataNow=ts.get_today_all()
#    dataNow=dataNow.set_index('code')
#    Lst=len(stockTrade) #close orders
#    if Lst:
#        todayT=today.date()
#        for i in range(Lst):
#            stocki=stockTrade[i]
#            stockTmp=pklData[stocki]
#            if dataNow.loc[stocki].low<=stockTmp[3]: #if touch stop loss
#                if dataNow.loc[stocki].open<=stockTmp[3]:
#                    stopReal=dataNow.loc[stocki].open
#                else:
#                    stopReal=stockTmp[3]
#                pklData['profits'].append(stopReal/stockTmp[1]-1.004)
#                pklData['stockTrade'].remove(stocki)
#                del pklData[stocki]
#            else:
#                datei=dataCall[stocks.index(stockTrade[i])].date.tolist()
#                tmp=datei.index(datetime.datetime.strftime(stockTmp[0],'%Y-%m-%d'))
#                holdDay=len(datei)-tmp+1
#                if holdDay>=stockTmp[2]+1:
#                    stopReal=dataNow.loc[stocki].trade
#                    pklData['profits'].append(stopReal/stockTmp[1]-1.004)
#                    pklData['stockTrade'].remove(stocki)
#                    del pklData[stocki]
#            if tradeTime:
#                tmp=open('X-Scan.pkl','wb')
#                pickle.dump(pklData,tmp)
#                tmp.close()                
#    features=[]
#    stocksTarget=[]
#    holds=[]
#    openPrice=[]
#    stopPrice=[]
#    for i in range(len(stocks)):
#        try:
#            tmpNow=dataNow.loc[stocks[i]]
#            opens=np.r_[dataCall[i].open, tmpNow.open]
#            closes=np.r_[dataCall[i].close, tmpNow.trade]
#            highs=np.r_[dataCall[i].high, tmpNow.high]
#            lows=np.r_[dataCall[i].low, tmpNow.low]
#            vols=np.r_[dataCall[i].volume, tmpNow.volume]
#        except:
#            continue
#        Li=len(opens)-1
#        
#        
#        for i2 in range(3,10):
#            if Li-3*i2-5<0:
#                break
#            if closes[Li]/closes[Li-1]>1.092:
#                continue                
#            if abs(max(highs[Li-3*i2-1:Li-3*i2+2])-max(highs[Li-3*i2-5:Li-2*i2+2]))<0.00000001 and \
#            abs(min(lows[Li-3*i2:Li-i2+1])-min(lows[Li-2*i2-1:Li-2*i2+2]))<0.00000001 and \
#            abs(max(highs[Li-2*i2:Li+1])-max(highs[Li-i2-1:Li-i2+2]))<0.00000001 and \
#            lows[Li]<min(lows[Li-i2:Li]) and \
#            min(highs[Li-3*i2-5:Li+1]-lows[Li-3*i2-5:Li+1])>0.0000001:
#                P1=np.argmax(highs[Li-3*i2-5:Li-2*i2+1]) #index 0 is i-3*i2-5
#                P2=np.argmin(lows[Li-2*i2-1:Li-2*i2+2])+i2+4
#                P3=np.argmax(highs[Li-i2-1:Li-i2+2])+2*i2+4
#                P4=3*i2+5
#                down1=P2-P1
#                up=P3-P2
#                down2=P4-P3
#                if max([down1,up,down2])-min([down1,up,down2])<2:
#                    baseI=Li-3*i2-5
#                    baseL=highs[baseI+P1]-lows[baseI+P2]
#                    try:
#                        baseE=sum(vols[baseI+P1-i2:baseI+P1])
#                        if baseE<1:
#                            continue
#                    except:
#                        continue                            
#                    features.append([(highs[baseI+P3]-lows[baseI+P2])/baseL,(highs[baseI+P3]-lows[baseI+P4])/baseL,\
#                                     sum(vols[baseI+P1+1:baseI+P2+1])/baseE,sum(vols[baseI+P2+1:baseI+P3+1])/baseE,\
#                                     sum(vols[baseI+P3+1:baseI+P4])/baseE])
#                    stocksTarget.append(stocks[i])
#                    holds.append(i2)
#                    openPrice.append(closes[-1])
#                    stopPrice.append(lows[-1])
#                    if fig>0:
#                        fig-=1
#                        plt.figure(figsize=(10,6))
#                        ax=plt.subplot()
#                        candleData=np.column_stack([range(P4+1),opens[baseI:Li+1],highs[baseI:Li+1],lows[baseI:Li+1],closes[baseI:Li+1]])
#                        mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
#                        plt.plot([P1,P2,P3,P4],[highs[baseI+P1],lows[baseI+P2],highs[baseI+P3],lows[baseI+P4]],color='k')
#                        plt.title(stocks[i])
#                        plt.grid()
#    if len(stocksTarget)>0:
#        stocksTarget=np.array(stocksTarget)
#        holds=np.array(holds)
#        ModelP=joblib.load('DownUpDownVol')
#        prob=ModelP.predict(xgb.DMatrix(data=features))
#        tmp=prob>0.5
#        probS=prob[tmp]
#        stockS=stocksTarget[tmp]
#        holdS=holds[tmp]
#        openPriceS=np.array(openPrice)[tmp]
#        stopPriceS=np.array(stopPrice)[tmp]
#        tmp=(-probS).argsort()
#        probS=probS[tmp]
#        stockS=stockS[tmp]
#        holdS=holdS[tmp]
#        openPriceS=openPriceS[tmp]
#        stopPriceS=stopPriceS[tmp]
#        stockTrade=[]
#        for i in range(len(stockS)):
#            print(stockS[i]+' win ratio:{}% and should be hold {} days'.format(round(probS[i]*100,2),holdS[i]))
#            pklData[stockS[i]]=[today.date(),openPriceS[i],holdS[i],stopPriceS[i],probS[i]]
#            stockTrade.append(stockS[i])
#        if tradeTime:
#            tmp=open('X-Scan.pkl','wb')
#            pklData['stockTrade'].extend(stockTrade)
#            pickle.dump(pklData,tmp)
#            tmp.close()
#    t2=datetime.datetime.now()
#    print('Time lapses {} minutes.'.format(round((t2-today).seconds/60,2)))

# -*- coding: utf-8 -*-
#"""
#Created on Wed Apr 11 17:15:20 2018
#
#@author: Administrator
#"""
#import tushare as ts
#import numpy as np
#import xgboost as xgb
#import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
#import datetime,pickle,pdb,joblib
#
#today=datetime.datetime.today()
##if 1: # only for the first time run
##    tmp=open('X-Scan.pkl','wb')
##    pklData={'dateSave':(today-datetime.timedelta(5)).date(),'profits':[],'stockTrade':[]}
##    pickle.dump(pklData,tmp)
##    tmp.close()    
#tradeTime=14<=today.hour<15 and today.minute>50
#tradeDay=0
#tmp=open('X-Scan.pkl','rb')
#pklData=pickle.load(tmp)
#tmp.close()
#fig=0
#if (today.date()-pklData['dateSave']).days>0:
#    tmp=ts.get_stock_basics()
#    stocks=tmp.index
#    L=len(stocks)
#    nDays=50 #number of natural days;
#    dataCall=[]
#    for i in range(L):
#        tmp=ts.get_k_data(code = stocks[i],start = datetime.datetime.strftime(today-datetime.timedelta(nDays),'%Y-%m-%d'))
#        dataCall.append(tmp)
#    #print('time lapse {} minutes.'.format(round((t2-today).seconds/60,2)))
#    pklData['dateSave']=today.date()
#    pklData['dataCall']=dataCall
#    pklData['stocks']=stocks
#    tmp=open('X-Scan.pkl','wb')
#    pickle.dump(pklData,tmp)
#    tmp.close()
#    t2=datetime.datetime.now()
#    print('Updating data has been completed now! and time lapses {} minutes.'.format(round((t2-today).seconds/60,2)))
#else:
#    stocks=pklData['stocks'].tolist()
#    stockTrade=pklData['stockTrade'].copy()
#    dataCall=pklData['dataCall']
#
#    if tradeDay:
#        dataNow=ts.get_today_all()
#        dataNow=dataNow.set_index('code')
#        Lst=len(stockTrade) #close orders
#        if Lst:
#            todayT=today.date()
#            for i in range(Lst):
#                stocki=stockTrade[i]
#                stockTmp=pklData[stocki]
#                if dataNow.loc[stocki].low<=stockTmp[3]: #if touch stop loss
#                    if dataNow.loc[stocki].open<=stockTmp[3]:
#                        stopReal=dataNow.loc[stocki].open
#                    else:
#                        stopReal=stockTmp[3]
#                    pklData['profits'].append(stopReal/stockTmp[1]-1.004)
#                    pklData['stockTrade'].remove(stocki)
#                    del pklData[stocki]
#                    print('close '+stocki)
#                else:
#                    datei=dataCall[stocks.index(stockTrade[i])].date.tolist()
#                    tmp=datei.index(datetime.datetime.strftime(stockTmp[0],'%Y-%m-%d'))
#                    holdDay=len(datei)-tmp+1
#                    if holdDay>=stockTmp[2]+1:
#                        stopReal=dataNow.loc[stocki].trade
#                        pklData['profits'].append(stopReal/stockTmp[1]-1.004)
#                        pklData['stockTrade'].remove(stocki)
#                        del pklData[stocki]
#                        print('close '+stocki)
#                if tradeTime and tradeDay:
#                    tmp=open('X-Scan.pkl','wb')
#                    pickle.dump(pklData,tmp)
#                    tmp.close()                
#    features=[]
#    stocksTarget=[]
#    holds=[]
#    openPrice=[]
#    stopPrice=[]
#    typeM=[] # label which type the model belongs to; 
#    for i in range(len(stocks)):
#        try:
#            if tradeDay:
#                tmpNow=dataNow.loc[stocks[i]]
#                opens=np.r_[dataCall[i].open, tmpNow.open]
#                closes=np.r_[dataCall[i].close, tmpNow.trade]
#                highs=np.r_[dataCall[i].high, tmpNow.high]
#                lows=np.r_[dataCall[i].low, tmpNow.low]
#                vols=np.r_[dataCall[i].volume, tmpNow.volume]
#            else:
#                opens=dataCall[i].open.values
#                closes=dataCall[i].close.values
#                highs=dataCall[i].high.values
#                lows=dataCall[i].low.values
#                vols=dataCall[i].volume.values
#        except:
#            continue
#        Li=len(opens)-1        
#        
#        for i2 in range(3,10): #DownUpDown
#            if Li-3*i2-5<0:
#                break
#            if closes[Li]/closes[Li-1]>1.092:
#                continue                
#            if abs(max(highs[Li-3*i2-1:Li-3*i2+2])-max(highs[Li-3*i2-5:Li-2*i2+2]))<0.00000001 and \
#            abs(min(lows[Li-3*i2:Li-i2+1])-min(lows[Li-2*i2-1:Li-2*i2+2]))<0.00000001 and \
#            abs(max(highs[Li-2*i2:Li+1])-max(highs[Li-i2-1:Li-i2+2]))<0.00000001 and \
#            lows[Li]<min(lows[Li-i2:Li]) and \
#            min(highs[Li-3*i2-5:Li+1]-lows[Li-3*i2-5:Li+1])>0.0000001:
#                P1=np.argmax(highs[Li-3*i2-5:Li-2*i2+1]) #index 0 is i-3*i2-5
#                P2=np.argmin(lows[Li-2*i2-1:Li-2*i2+2])+i2+4
#                P3=np.argmax(highs[Li-i2-1:Li-i2+2])+2*i2+4
#                P4=3*i2+5
#                down1=P2-P1
#                up=P3-P2
#                down2=P4-P3
#                if max([down1,up,down2])-min([down1,up,down2])<2:
#                    baseI=Li-3*i2-5
#                    baseL=highs[baseI+P1]-lows[baseI+P2]
#                    try:
#                        baseE=sum(vols[baseI+P1-i2:baseI+P1])
#                        if baseE<1:
#                            continue
#                    except:
#                        continue                            
#                    features.append([(highs[baseI+P3]-lows[baseI+P2])/baseL,(highs[baseI+P3]-lows[baseI+P4])/baseL,\
#                                     sum(vols[baseI+P1+1:baseI+P2+1])/baseE,sum(vols[baseI+P2+1:baseI+P3+1])/baseE,\
#                                     sum(vols[baseI+P3+1:baseI+P4])/baseE])
#                    stocksTarget.append(stocks[i])
#                    holds.append(i2)
#                    openPrice.append(closes[-1])
#                    stopPrice.append(lows[-1])
#                    typeM.append('DownUpDownVol')
#            
#        for i2 in range(4,20): #UpDown
#            if Li-3*i2//2-3<0:
#                break
#            if closes[Li]/closes[Li-1]>1.092:
#                continue            
#            if abs(min(lows[Li-i2-5:Li-i2+3])-lows[Li-i2])<0.00000001:
#                highT=np.argmax(highs[Li-i2:Li+1])+Li-i2
#                if abs(2*(highT-Li)+i2)<2 and \
#                lows[Li-i2]<min(lows[Li-i2+1:highT+1]) and\
#                lows[Li]<min(lows[highT:Li]) and\
#                min(highs[Li-3*i2//2-3:Li+1]-lows[Li-3*i2//2-3:Li+1])>0.0000001: # avoid no trading day;
#                    up=highs[highT]-lows[Li-i2]
#                    down=highs[highT]-lows[Li]
#                    try:
#                        baseE=sum(vols[Li-i2-i2//2:Li-i2])
#                        if baseE<1:
#                            continue
#                    except:
#                        continue                        
#                    features.append([down/up,sum(vols[highT:Li])/baseE,sum(vols[Li-i2:highT])/baseE])
#                    stocksTarget.append(stocks[i])
#                    holds.append(i2)
#                    openPrice.append(closes[-1])
#                    stopPrice.append(lows[-1])
#                    typeM.append('UpDownVol')
#                   
##                    if fig>0:
##                        fig-=1
##                        plt.figure(figsize=(10,6))
##                        ax=plt.subplot()
##                        candleData=np.column_stack([range(P4+1),opens[baseI:Li+1],highs[baseI:Li+1],lows[baseI:Li+1],closes[baseI:Li+1]])
##                        mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
##                        plt.plot([P1,P2,P3,P4],[highs[baseI+P1],lows[baseI+P2],highs[baseI+P3],lows[baseI+P4]],color='k')
##                        plt.title(stocks[i])
##                        plt.grid()
#    if len(stocksTarget)>0:
#        typeM=np.array(typeM)
#        stocksTarget=np.array(stocksTarget)
#        holds=np.array(holds)
#        openPrice=np.array(openPrice)
#        stopPrice=np.array(stopPrice)
#        features=np.array(features)
#        
#        indexT=np.where(typeM=='DownUpDownVol')[0]        
#        if indexT.sum():
#            ModelP=joblib.load('DownUpDownVol')
#            tmpF=[]
#            for i in indexT:
#                tmpF.append(features[i])
#            prob=ModelP.predict(xgb.DMatrix(data=tmpF)) 
#            tmp=prob>0.5
#            probS=prob[tmp]
#            stockS=stocksTarget[indexT][tmp]
#            holdS=holds[indexT][tmp]
#            openPriceS=openPrice[indexT][tmp]
#            stopPriceS=stopPrice[indexT][tmp]
#            typeS=['DownUpDownVol']*len(stopPriceS)
#        indexT=np.where(typeM=='UpDownVol')[0]        
#        if indexT.sum():
#            ModelP=joblib.load('UpDownVol')
#            tmpF=[]
#            for i in indexT:
#                tmpF.append(features[i])
#            prob=ModelP.predict(xgb.DMatrix(data=tmpF)) 
#            tmp=prob>0.65
#            probS=np.r_[probS,prob[tmp]]
#            stockS=np.r_[stockS,stocksTarget[indexT][tmp]]
#            holdS=np.r_[holdS,holds[indexT][tmp]]
#            openPriceS=np.r_[openPriceS,openPrice[indexT][tmp]]
#            stopPriceS=np.r_[stopPriceS,stopPrice[indexT][tmp]]
#            typeS=np.r_[typeS,['UpDownVol']*len(prob[tmp])]
#            
#        tmp=(probS).argsort()
#        probS=probS[tmp]
#        stockS=stockS[tmp]
#        holdS=holdS[tmp]
#        openPriceS=openPriceS[tmp]
#        stopPriceS=stopPriceS[tmp]
#        typeS=typeS[tmp]
#        stockTrade=[]
#        for i in range(len(stockS)):
#            print(stockS[i]+' win ratio:{}% and should be hold {} days;Model is {}'.format(round(probS[i]*100,2),holdS[i],typeS[i]))
#            pklData[stockS[i]]=[today.date(),openPriceS[i],holdS[i],stopPriceS[i],probS[i]]
#            stockTrade.append(stockS[i])
#        if tradeTime and tradeDay:
#            tmp=open('X-Scan.pkl','wb')
#            pklData['stockTrade'].extend(stockTrade)
#            pickle.dump(pklData,tmp)
#            tmp.close()
#    t2=datetime.datetime.now()
#    print('Time lapses {} minutes.'.format(round((t2-today).seconds/60,2)))


#import tushare as ts
#import numpy as np
##import xgboost as xgb
#import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
#import datetime,time,shutil,os,pickle,pdb
#
#backDay=0
#showHere=0
#reload=0
#
#todayTime=datetime.datetime.today()
#today=todayTime.date()
#saveFolder='e:\stockSelect' #save stocks' pictures which were selected.
#tradeDay= (not ts.is_holiday(datetime.datetime.strftime(today,'%Y-%m-%d'))) and todayTime.hour*100+todayTime.minute>930
#try:
#    tmp=open('scan_trade.pkl','rb')
#    pklData=pickle.load(tmp)
#    tmp.close()
#    todayLast=pklData['today']
#    dataCall=pklData['dataCall']
#    stocks=pklData['stocks']
#except:
#    todayLast=0
#if today!=todayLast or reload:
#    tmp=ts.get_stock_basics()
#    stocks=tmp.index
#    L=len(stocks)
#    nDays=260+int(1.5*backDay) #number of natural days;
#    dataCall=[]
#    t1=time.time()
#    for i in range(L):
#        tmp=ts.get_k_data(code = stocks[i],start = datetime.datetime.strftime(today-datetime.timedelta(nDays),'%Y-%m-%d'))
#        dataCall.append(tmp)
#        ratioStocks=(i+1)/L
#        t2=time.time()
#        print(stocks[i]+':'+str(round(100*ratioStocks,2))+'%,and need more time:{} minutes'.format(round((t2-t1)*(1/ratioStocks-1)/60,2)))
#    
#    t2=datetime.datetime.now()
#    print('Updating data has been completed now! and time lapses {} minutes.'.format(round((t2-todayTime).seconds/60,2)))
#    pklData={'today':today,'dataCall':dataCall,'stocks':stocks}
#    tmp=open('scan_trade.pkl','wb')
#    pickle.dump(pklData,tmp)
#    tmp.close()
#
#if tradeDay:
#    dataNow=ts.get_today_all()
#    dataNow=dataNow.set_index('code')
#stockPass=[]
#stockSelect=[]
#try:
#    shutil.rmtree(saveFolder)
#except:
#    pass
#os.mkdir(saveFolder)
#for i in range(len(stocks)):
#    if len(dataCall[i])<1:
#        stockPass.append(stocks[i])
#        continue
#    if tradeDay:
#        tmpNow=dataNow.loc[stocks[i]]
#        opens=np.r_[dataCall[i].open, tmpNow.open]
#        closes=np.r_[dataCall[i].close, tmpNow.trade]
#        highs=np.r_[dataCall[i].high, tmpNow.high]
#        lows=np.r_[dataCall[i].low, tmpNow.low]
#        vols=np.r_[dataCall[i].volume, tmpNow.volume/100]
#    else:
#        opens=dataCall[i].open.values
#        closes=dataCall[i].close.values
#        highs=dataCall[i].high.values
#        lows=dataCall[i].low.values
#        vols=dataCall[i].volume.values
#    Li=len(opens)-1
#    for i2 in range(4,20):
#        if Li-3*i2-5-backDay<0:
#            break               
#        pointZero=Li-6*i2
#        if pointZero-backDay-1<0:
#            pointZero=backDay+1
#        if abs(max(highs[Li-3*i2-4-backDay:Li-3*i2+4-backDay])-max(highs[pointZero-backDay-1:Li-2*i2+1-backDay]))<0.00000001 and \
#        abs(min(lows[Li-3*i2-backDay-1:Li-i2-backDay])-min(lows[Li-2*i2-3-backDay:Li-2*i2+3-backDay]))<0.00000001 and \
#        abs(max(highs[Li-2*i2-backDay-1:Li-backDay])-max(highs[Li-i2-2-backDay:Li-i2+2-backDay]))<0.00000001 and \
#        lows[Li-backDay]<min(lows[Li-i2-backDay-2:Li-backDay]) and \
#        min(highs[Li-3*i2-5-backDay-1:Li-backDay]-lows[Li-3*i2-5-backDay-1:Li-backDay])>0.0000001 and \
#        highs[Li-backDay]<highs[Li-backDay-1]:
#            addDays=9*i2
#            if Li-3*i2-addDays-backDay<0:
#                addDays=Li-3*i2-backDay
#            P1=np.argmax(highs[Li-3*i2-addDays-backDay:Li-2*i2-backDay])
#            P2=np.argmin(lows[Li-3*i2-backDay:Li-2*i2+3-backDay])+addDays
#            P3=np.argmax(highs[Li-2*i2-backDay:Li-i2+3-backDay])+i2+addDays
#            P4=3*i2+addDays
#            baseI=Li-3*i2-addDays-backDay
#            down1=P2-P1
#            up=P3-P2
#            down2=P4-P3      
#            fig=plt.figure(figsize=(10,6))
#            if max([down1,up,down2])-min([down1,up,down2])<2:# and fig>0:
#                periodBoll=i2*3
#                upLine=[]
#                middleLine=[]
#                downLine=[]
#                for i3 in range(baseI+periodBoll,Li+1):#periodBoll-1,Li+1-baseI
#                    tmpMean=closes[i3-periodBoll+1:i3+1].mean()
#                    tmpStd=closes[i3-periodBoll+1:i3+1].std()
#                    upLine.append(tmpMean+2*tmpStd)
#                    middleLine.append(tmpMean)
#                    downLine.append(tmpMean-2*tmpStd)                   
#                ax=fig.add_axes([0.1,0.3,0.8,0.6])
#                ax.plot(range(periodBoll,Li+1-baseI),upLine,'r--')
#                ax.plot(range(periodBoll,Li+1-baseI),middleLine,'b--')
#                ax.plot(range(periodBoll,Li+1-baseI),downLine,'r--')
#                ax.plot([P1,P2,P3,P4],[highs[baseI+P1],lows[baseI+P2],highs[baseI+P3],lows[baseI+P4]],color='k')
#                upTmp=highs[baseI+P3]-lows[baseI+P2]
#                ax.text(P1,highs[baseI+P1],round((highs[baseI+P1]-lows[baseI+P2])/upTmp,3))
#                ax.text(P3,highs[baseI+P3],round((highs[baseI+P3]-lows[baseI+P4])/upTmp,3))
#                candleData=np.column_stack([range(P4+backDay+1),opens[baseI:Li+1],highs[baseI:Li+1],lows[baseI:Li+1],closes[baseI:Li+1]])
#                mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
#                bars=len(opens[baseI:Li+1])
#                ax.set_xticks(range(0,bars,3))
#                ax.grid()
#                plt.title(stocks[i])
#                ax1=fig.add_axes([0.1,0.1,0.8,0.2])
#                vol=vols[baseI:Li+1]
#                ax1.bar(range(len(vol)),vol)
#                ax1.set_xticks(range(0,bars,3))
#                ax1.grid()
#                plt.savefig(saveFolder+'\\'+stocks[i])
#                if showHere:
#                    plt.show()
#                plt.clf()
#                stockSelect.append(stocks[i])
#                
#print('Stocks which are past: '+','.join(stockPass))
#print('Stocks which are select: ',end='')
#print(stockSelect)

import tushare as ts
import numpy as np
#import xgboost as xgb
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import datetime,time,shutil,os,pickle,pdb

backDay=3
showHere=1
diffBars=1
reload=0

saveFolder='e:\stockSelect' #save stocks' pictures which were selected.
if reload:
    todayTime=datetime.datetime.today()
    today=todayTime.date()    
    tradeDay= (not ts.is_holiday(datetime.datetime.strftime(today,'%Y-%m-%d'))) and todayTime.hour*100+todayTime.minute>930
    try:
        tmp=open('scan_trade.pkl','rb')
        pklData=pickle.load(tmp)
        tmp.close()
        todayLast=pklData['today']
        dataCall=pklData['dataCall']
        stocks=pklData['stocks']
    except:
        todayLast=0
    if today!=todayLast:
        tmp=ts.get_stock_basics()
        stocks=tmp.index
        L=len(stocks)
        nDays=260+int(1.5*backDay) #number of natural days;
        dataCall=[]
        t1=time.time()
        for i in range(L):
            tmp=ts.get_k_data(code = stocks[i],start = datetime.datetime.strftime(today-datetime.timedelta(nDays),'%Y-%m-%d'))
            dataCall.append(tmp)
            ratioStocks=(i+1)/L
            t2=time.time()
            print(stocks[i]+':'+str(round(100*ratioStocks,2))+'%,and need more time:{} minutes'.format(round((t2-t1)*(1/ratioStocks-1)/60,2)))
        
        t2=datetime.datetime.now()
        print('Updating data has been completed now! and time lapses {} minutes.'.format(round((t2-todayTime).seconds/60,2)))
        pklData={'today':today,'dataCall':dataCall,'stocks':stocks}
        tmp=open('scan_trade.pkl','wb')
        pickle.dump(pklData,tmp)
        tmp.close()
    
    if tradeDay:
        dataNow=ts.get_today_all()
        dataNow=dataNow.set_index('code')
else:
    tmp=open('scan_trade.pkl','rb')
    pklData=pickle.load(tmp)
    tmp.close()
    today=pklData['today']
    dataCall=pklData['dataCall']
    stocks=pklData['stocks']
    tradeDay=0
stockPass=[]
stockSelect=[]
try:
    shutil.rmtree(saveFolder)
except:
    pass
os.mkdir(saveFolder)
for i in range(len(stocks)):
    if len(dataCall[i])<1:
        stockPass.append(stocks[i])
        continue
    if tradeDay:
        try:
            tmpNow=dataNow.loc[stocks[i]]
            opens=np.r_[dataCall[i].open, tmpNow.open]
            closes=np.r_[dataCall[i].close, tmpNow.trade]
            highs=np.r_[dataCall[i].high, tmpNow.high]
            lows=np.r_[dataCall[i].low, tmpNow.low]
            vols=np.r_[dataCall[i].volume, tmpNow.volume/100]
        except:
            print('cant download current data for '+stocks[i])
            continue
    else:
        opens=dataCall[i].open.values
        closes=dataCall[i].close.values
        highs=dataCall[i].high.values
        lows=dataCall[i].low.values
        vols=dataCall[i].volume.values
    Li=len(opens)-1
    dataCollect=[]
    for i2 in range(4,20):
        if Li-3*i2-6-backDay<0:
            break               
        pointZero=Li-6*i2
        if pointZero-backDay-1<0:
            pointZero=backDay+1
        if abs(max(highs[Li-3*i2-4-backDay:Li-3*i2+4-backDay])-max(highs[pointZero-backDay-1:Li+1-backDay]))<0.00000001 and \
        abs(min(lows[Li-3*i2-backDay-1:Li-i2-backDay])-min(lows[Li-2*i2-3-backDay:Li-2*i2+3-backDay]))<0.00000001 and \
        abs(max(highs[Li-2*i2-backDay-1:Li-backDay])-max(highs[Li-i2-2-backDay:Li-i2+2-backDay]))<0.00000001 and \
        (lows[Li-backDay]<min(lows[Li-i2-backDay-2:Li-backDay]) or \
        (highs[Li-backDay]<highs[Li-backDay-1] and lows[Li-1-backDay]<min(lows[Li-i2-backDay-2:Li-backDay]) )) and \
        min(highs[Li-3*i2-6-backDay:Li-backDay]-lows[Li-3*i2-6-backDay:Li-backDay])>0.0000001 :
            addDays=9*i2
            if Li-3*i2-addDays-backDay<0:
                addDays=Li-3*i2-backDay
            P1=np.argmax(highs[Li-3*i2-addDays-backDay:Li-2*i2-backDay])
            P2=np.argmin(lows[Li-3*i2-backDay:Li-2*i2+3-backDay])+addDays
            P3=np.argmax(highs[Li-2*i2-backDay:Li-i2+3-backDay])+i2+addDays
            P4=3*i2+addDays
            baseI=Li-3*i2-addDays-backDay
            down1=P2-P1
            up=P3-P2
            down2=P4-P3
            if i2>8:
                DBtmp=diffBars+1
            else:
                DBtmp=diffBars
            startTmp=max(0,Li-backDay-int(3.5*(P4-P1))-4)
            if max([down1,up,down2])-min([down1,up,down2])<=DBtmp:# \
#            and min(lows[Li-3*i2-4-backDay:Li+1-backDay])>min(lows[startTmp:Li-backDay+1])+0.45*(max(highs[startTmp:Li-backDay+1])-min(lows[startTmp:Li-backDay+1])):# and fig>0:
                periodBoll=20#i2*3  #################################
                upLine=[]
                middleLine=[]
                downLine=[]
                for i3 in range(baseI+periodBoll,Li+1):#periodBoll-1,Li+1-baseI
                    tmpMean=closes[i3-periodBoll+1:i3+1].mean()
                    tmpStd=closes[i3-periodBoll+1:i3+1].std()
                    upLine.append(tmpMean+2*tmpStd)
                    middleLine.append(tmpMean)
                    downLine.append(tmpMean-2*tmpStd)
                dataCollect.append([range(periodBoll,Li+1-baseI),[upLine,middleLine,downLine],[P1,P2,P3,P4],\
                                    [highs[baseI+P1],lows[baseI+P2],highs[baseI+P3],lows[baseI+P4]],\
                                    baseI])
    LdataCollect=len(dataCollect)
    if LdataCollect:
        fig=plt.figure(figsize=(10,6))
        ax=fig.add_axes([0.1,0.3,0.8,0.6])                     
        monitorTmp=[]
        monitorInd=[]
        baseRec=[]
        for i2 in range(LdataCollect):
            datai2=(np.array(dataCollect[i2][2])+dataCollect[i2][4]).tolist()
            if datai2 not in monitorTmp:
                monitorTmp.append(datai2)
                monitorInd.append(i2)
                baseRec.append(dataCollect[i2][4])
        baseImin=min(baseRec)
        for i2 in monitorInd:
            bollx=dataCollect[i2][0]
            bollLine=dataCollect[i2][1]
            ax.plot(bollx,bollLine[0],'r--',bollx,bollLine[1],'b--',bollx,bollLine[2],'r--')
            P1,P2,P3,P4=dataCollect[i2][2][0],dataCollect[i2][2][1],dataCollect[i2][2][2],dataCollect[i2][2][3]
#            price4=dataCollect[i2][3]
            baseI=dataCollect[i2][4]            
            baseIadd=baseI-baseImin
            ax.plot([baseIadd+P1,baseIadd+P2,baseIadd+P3,baseIadd+P4],[highs[baseI+P1],lows[baseI+P2],highs[baseI+P3],lows[baseI+P4]],color='k')
            upTmp=highs[baseI+P3]-lows[baseI+P2]
            ax.text(baseIadd+P1,highs[baseI+P1],round((highs[baseI+P1]-lows[baseI+P2])/upTmp,3))
            ax.text(baseIadd+P3,highs[baseI+P3],round((highs[baseI+P3]-lows[baseI+P4])/upTmp,3))
        
        candleData=np.column_stack([range(baseIadd+P4+backDay+1),opens[baseI-baseIadd:Li+1],highs[baseI-baseIadd:Li+1],lows[baseI-baseIadd:Li+1],closes[baseI-baseIadd:Li+1]])
        mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
        bars=len(opens[baseI:Li+1])
        ax.set_xticks(range(0,bars,3))
        ax.grid()
        plt.title(stocks[i])
        ax1=fig.add_axes([0.1,0.1,0.8,0.2])
        vol=vols[baseI-baseIadd:Li+1]
        ax1.bar(range(len(vol)),vol)
        ax1.set_xticks(range(0,bars,3))
        ax1.grid()
        plt.savefig(saveFolder+'\\'+stocks[i])
        if not showHere:
            plt.clf()
        stockSelect.append(stocks[i])
                
print('Stocks which are past: '+','.join(stockPass))
print('Stocks which are select: ',end='')
print(stockSelect)





