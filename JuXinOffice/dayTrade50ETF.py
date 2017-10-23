# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:36:46 2017

@author: Administrator
"""
from WindPy import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import datetime,pickle,pdb,time
t1=time.clock()

timeStart='2014-01-01'
timeEnd=(datetime.date.today()-timedelta(days=1)).strftime('%Y-%m-%d')

stopAbsList=np.linspace(0.001,0.015,10)
stopMovList=np.linspace(0.001,0.020,20)
ratioVList=[0.6,0.8,0.9,1.1,1.3,1.5,1.7]
fig=2

try:
    tem=open('dayTrade50ETF','rb')
    dataPKL=pickle.load(tem)
    tem.close()
    opens=dataPKL['opens']
    closes=dataPKL['closes']
    highs=dataPKL['highs']
    lows=dataPKL['lows']
    vols=dataPKL['vols']
    times=dataPKL['times']
    openT=dataPKL['openT']
    closeT=dataPKL['closeT']
    highT=dataPKL['highT']
    lowT=dataPKL['lowT']
    volT=dataPKL['volT']
except:
    w.start()
    dataTem=w.wsi('IH.CFE','open,high,low,close,volume',timeStart+' 09:00:00',timeEnd+' 15:01:00','periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
    opens=dataTem.Data[0]
    highs=dataTem.Data[1]
    lows=dataTem.Data[2]
    closes=dataTem.Data[3]
    vols=dataTem.Data[4]
    times=dataTem.Times
    dataTem=w.wsi('510050.SH','open,high,low,close,volume',timeStart+' 09:00:00',timeEnd+' 15:01:00','periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
    openT=dataTem.Data[0]
    highT=dataTem.Data[1]
    lowT=dataTem.Data[2]
    closeT=dataTem.Data[3]
    volT=dataTem.Data[4]   
    dataPKL={'opens':opens,'highs':highs,'lows':lows,'closes':closes,'vols':vols,'times':times,\
             'openT':openT,'highT':highT,'lowT':lowT,'closeT':closeT,'volT':volT}
    tem=open('dayTrade50ETF','wb')
    pickle.dump(dataPKL,tem)
    tem.close()
loops=len(opens)//241
ReAll=[]
stop=[]
maxOrder=1

BarMean=[5,10,20,30,60,80]
for dayMean in BarMean:
    allLoop=len(stopAbsList)*len(stopMovList)*len(ratioVList)
    nowLoop=1
    for j1 in stopAbsList:
        for j2 in stopMovList:
            for j3 in ratioVList:
                ti=time.clock()
                stopAbs=j1
                stopMov=j2
                ratioV=j3
                Re=[]
                for i in range(loops):
                    Open=opens[i*241:(i+1)*241]
                    Close=closes[i*241:(i+1)*241]
                    High=highs[i*241:(i+1)*241]
                    Low=lows[i*241:(i+1)*241]
                    Vol=vols[i*241:(i+1)*241]
                    CloseT=closeT[i*241:(i+1)*241]
                    OpenT=openT[i*241:(i+1)*241]
                    i2=dayMean
                    xi1=[]
                    xi2=[]
                    yi1=[]    
                    yi2=[]
                    colori=[]
                    while i2<236:
                        maxV=np.max(Vol[i2-dayMean:i2])
                        if Vol[i2]>maxV*ratioV and Vol[i2+1]>maxV*ratioV:
                            priceOpenT=[OpenT[i2+3]]
                            priceOpen=[Open[i2+3]]
                            barOpen=[i2+3]
                            priceClose=[]
                            if round(Close[i2+2],3)>=round(Open[i2+2],3):
                                Hold=1
                            else:
                                Hold=0#-1
                                barOpen.pop()
                            for i3 in range(i2+3,241):
                                if Hold>0:
                                    closeTem=-1
                                    if Low[i3]<=priceOpen[-1]-stopAbs or max(High[barOpen[0]:i3+1])-Low[i3]>=stopMov:
                                        closeTem=CloseT[i3]
                                    if closeTem>0:
                                        for i4 in range(Hold):
                                            Re.append(closeTem/priceOpenT[i4]-1.0004)
                                            priceClose.append(closeTem)
                                        break
                                    elif abs(Hold)<maxOrder:
                                        maxVtem=np.max(Vol[i3-dayMean:i3])
                                        if i3+3<=240 and Vol[i3]>maxVtem*ratioV and Vol[i3+1]>maxVtem*ratioV \
                                        and round(Close[i3+2],3)>=round(Open[i3+2],3) :
                                            Hold=Hold+1
                                            priceOpenT.append(OpenT[i3+3])
                                            priceOpen.append(Open[i3+3])
                                            barOpen.append(i3+3)                                    
                                elif Hold<0:
                                    closeTem=-1
                                    if High[i3]>=priceOpen[-1]+stopAbs or High[i3]-min(Low[barOpen[0]:i3+1])>=stopMov:
                                        closeTem=CloseT[i3]
                                    if closeTem>0:
                                        for i4 in range(-Hold):
                                            Re.append(1-closeTem/priceOpenT[i4]-0.0004)
                                            priceClose.append(closeTem)
                                        break
                                    elif abs(Hold)<maxOrder:
                                        maxVtem=np.max(Vol[i3-dayMean:i3])
                                        if i3+3<=240 and Vol[i3]>maxVtem*ratioV and Vol[i3+1]>maxVtem*ratioV \
                                        and round(Close[i3+2],3)<round(Open[i3+2],3) :
                                            Hold=Hold-1
                                            priceOpenT.append(OpenT[i3+3])
                                            priceOpen.append(Open[i3+3])
                                            barOpen.append(i3+3)              
                                    
                                if i3==240:
                                    for i4 in range(abs(Hold)):
                                        Re.append((CloseT[i3]-priceOpenT[i4])*(Hold>0)/priceOpenT[i4]-0.0004)  
                                        priceClose.append(CloseT[i3])
                            i2=i3
                            Lorder=len(barOpen)
                            for i4 in range(Lorder):
                                xi1.append(barOpen[i4])
                                xi2.append(i3)
                                yi1.append(priceOpenT[i4])
                                yi2.append(priceClose[i4])
                                if Re[-Lorder+i4]>0:
                                    colori.append('purple')
                                else:
                                    colori.append('cyan')
                        else:
                            i2=i2+1
                        
                    if fig>0 and len(xi1)>=2:
                        fig=fig-1
                        plt.figure(figsize=(25,8))
                        ax=plt.subplot2grid((3,1),(0,0),rowspan=2)
                        plt.title(times[i*241].strftime('%Y-%m-%d'))
                        candleData=np.column_stack([list(range(len(Open))),Open,High,Low,Close])
                        mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
                        for i2 in range(len(colori)):
                            ax.plot([xi1[i2],xi2[i2]],[yi1[i2],yi2[i2]],colori[i2],linewidth=3)
                        plt.xticks(range(len(Open))[::5])
                        plt.grid()
                        ax1=plt.subplot2grid((3,1),(2,0))
                        ax1.bar(range(len(Vol)),Vol)
                        plt.xticks(range(len(Open))[::5])
                        plt.grid()
                
                ReAll.append(Re)
                stop.append([stopAbs,stopMov,ratioV])
                print('process %d/%d; time left:%.1f minutes.' %(nowLoop,allLoop,(ti-t1)*(allLoop/nowLoop-1)/60))
                nowLoop=nowLoop+1
                #plt.figure()
                #plt.plot(np.cumsum(Re))
    indMax=np.argsort(list(map(sum,ReAll)))[-1]
    plt.figure(figsize=(25,8))
    plt.plot(np.cumsum(ReAll[indMax]))
    plt.title('stopAbs:'+str(stop[indMax][0])+';stopMove:'+str(stop[indMax][1])+';ratioV:'+str(stop[indMax][2]) )
    plt.savefig('C:/Users/Administrator/Desktop/BarMax'+str(dayMean))


t2=time.clock()
print('time lapse:%.1f minutes' % ((t2-t1)/60))




## pure 50ETF
#from WindPy import *
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
#import datetime,pickle,pdb,time
#t1=time.clock()
#
#timeStart='2014-01-01'
#timeEnd=(datetime.date.today()-timedelta(days=1)).strftime('%Y-%m-%d')
#
#stopAbsList=np.linspace(0.001,0.015,10)
#stopMovList=np.linspace(0.001,0.020,20)
#ratioVList=[0.6,0.8,0.9,1.1,1.3,1.5,1.7]
#fig=2
#
#try:
#    tem=open('dayTrade50ETF','rb')
#    dataPKL=pickle.load(tem)
#    tem.close()
#    opens=dataPKL['opens']
#    closes=dataPKL['closes']
#    highs=dataPKL['highs']
#    lows=dataPKL['lows']
#    vols=dataPKL['vols']
#    times=dataPKL['times']
#except:
#    w.start()
#    dataTem=w.wsi('IH.CFE','open,high,low,close,volume',timeStart+' 09:00:00',timeEnd+' 15:01:00','periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
#    opens=dataTem.Data[0]
#    highs=dataTem.Data[1]
#    lows=dataTem.Data[2]
#    closes=dataTem.Data[3]
#    vols=dataTem.Data[4]
#    times=dataTem.Times
#    dataPKL={'opens':opens,'highs':highs,'lows':lows,'closes':closes,'vols':vols,'times':times}
#    tem=open('dayTrade50ETF','wb')
#    pickle.dump(dataPKL,tem)
#    tem.close()
#loops=len(opens)//241
#ReAll=[]
#stop=[]
#maxOrder=5
#
#BarMean=[5,10,20,30,60,80]
#for dayMean in BarMean:
#    allLoop=len(stopAbsList)*len(stopMovList)*len(ratioVList)
#    nowLoop=1
#    for j1 in stopAbsList:
#        for j2 in stopMovList:
#            for j3 in ratioVList:
#                ti=time.clock()
#                stopAbs=j1
#                stopMov=j2
#                ratioV=j3
#                Re=[]
#                for i in range(loops):
#                    Open=opens[i*241:(i+1)*241]
#                    Close=closes[i*241:(i+1)*241]
#                    High=highs[i*241:(i+1)*241]
#                    Low=lows[i*241:(i+1)*241]
#                    Vol=vols[i*241:(i+1)*241]
#                    CloseT=closeT[i*241:(i+1)*241]
#                    i2=dayMean
#                    xi1=[]
#                    xi2=[]
#                    yi1=[]    
#                    yi2=[]
#                    colori=[]
#                    while i2<236:
#                        maxV=np.max(Vol[i2-dayMean:i2])
#                        if Vol[i2]>maxV*ratioV and Vol[i2+1]>maxV*ratioV:
#                            priceOpen=[Open[i2+3]]
#                            barOpen=[i2+3]
#                            priceClose=[]
#                            if round(Close[i2+2],3)>=round(Open[i2+2],3):
#                                Hold=1
#                            else:
#                                Hold=-1
#                            for i3 in range(i2+3,241):
#                                if Hold>0:
#                                    closeTem=-1
#                                    if Low[i3]<=priceOpen[-1]-stopAbs:
#                                        closeTem=priceOpen[-1]-stopAbs
#                                    elif max(High[barOpen[0]:i3+1])-Low[i3]>=stopMov:
#                                        closeTem=max(High[barOpen[0]:i3+1])-stopMov
#                                    if closeTem>0:
#                                        for i4 in range(Hold):
#                                            Re.append(closeTem/priceOpen[i4]-1.0004)
#                                            priceClose.append(closeTem)
#                                        break
#                                    elif abs(Hold)<maxOrder:
#                                        maxVtem=np.max(Vol[i3-dayMean:i3])
#                                        if i3+3<=240 and Vol[i3]>maxVtem*ratioV and Vol[i3+1]>maxVtem*ratioV \
#                                        and round(Close[i3+2],3)>=round(Open[i3+2],3) :
#                                            Hold=Hold+1
#                                            priceOpen.append(Open[i3+3])
#                                            barOpen.append(i3+3)                                    
#                                elif Hold<0:
#                                    closeTem=-1
#                                    if High[i3]>=priceOpen[-1]+stopAbs:
#                                        closeTem=priceOpen[-1]+stopAbs
#                                    elif High[i3]-min(Low[barOpen[0]:i3+1])>=stopMov:
#                                        closeTem=min(Low[barOpen[0]:i3+1])+stopMov
#                                    if closeTem>0:
#                                        for i4 in range(-Hold):
#                                            Re.append(1-closeTem/priceOpen[i4]-0.0004)
#                                            priceClose.append(closeTem)
#                                        break
#                                    elif abs(Hold)<maxOrder:
#                                        maxVtem=np.max(Vol[i3-dayMean:i3])
#                                        if i3+3<=240 and Vol[i3]>maxVtem*ratioV and Vol[i3+1]>maxVtem*ratioV \
#                                        and round(Close[i3+2],3)<round(Open[i3+2],3) :
#                                            Hold=Hold-1
#                                            priceOpen.append(Open[i3+3])
#                                            barOpen.append(i3+3)              
#                                    
#                                if i3==240:
#                                    for i4 in range(abs(Hold)):
#                                        Re.append((Close[i3]-priceOpen[i4])*(Hold>0)/priceOpen[i4]-0.0004)  
#                                        priceClose.append(Close[i3])
#                            i2=i3
#                            Lorder=len(barOpen)
#                            for i4 in range(Lorder):
#                                xi1.append(barOpen[i4])
#                                xi2.append(i3)
#                                yi1.append(priceOpen[i4])
#                                yi2.append(priceClose[i4])
#                                if Re[-Lorder+i4]>0:
#                                    colori.append('purple')
#                                else:
#                                    colori.append('cyan')
#                        else:
#                            i2=i2+1
#                        
#                    if fig>0 and len(xi1)>=2:
#                        fig=fig-1
#                        plt.figure(figsize=(25,8))
#                        ax=plt.subplot2grid((3,1),(0,0),rowspan=2)
#                        plt.title(times[i*241].strftime('%Y-%m-%d'))
#                        candleData=np.column_stack([list(range(len(Open))),Open,High,Low,Close])
#                        mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
#                        for i2 in range(len(colori)):
#                            ax.plot([xi1[i2],xi2[i2]],[yi1[i2],yi2[i2]],colori[i2],linewidth=3)
#                        plt.xticks(range(len(Open))[::5])
#                        plt.grid()
#                        ax1=plt.subplot2grid((3,1),(2,0))
#                        ax1.bar(range(len(Vol)),Vol)
#                        plt.xticks(range(len(Open))[::5])
#                        plt.grid()
#                
#                ReAll.append(Re)
#                stop.append([stopAbs,stopMov,ratioV])
#                print('process %d/%d; time left:%.1f minutes.' %(nowLoop,allLoop,(ti-t1)*(allLoop/nowLoop-1)/60))
#                nowLoop=nowLoop+1
#                #plt.figure()
#                #plt.plot(np.cumsum(Re))
#    indMax=np.argsort(list(map(sum,ReAll)))[-1]
#    plt.figure(figsize=(25,8))
#    plt.plot(np.cumsum(ReAll[indMax]))
#    plt.title('stopAbs:'+str(stop[indMax][0])+';stopMove:'+str(stop[indMax][1])+';ratioV:'+str(stop[indMax][2]) )
#    plt.savefig('C:/Users/Administrator/Desktop/BarMax'+str(dayMean))
#
#
#t2=time.clock()
#print('time lapse:%.1f minutes' % ((t2-t1)/60))






#from WindPy import *
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
#import datetime,pickle,pdb
#
#
#timeStart='2014-01-01'
#timeEnd=(datetime.date.today()-timedelta(days=1)).strftime('%Y-%m-%d')
#
#stopAbsList=np.linspace(0.001,0.015,10)
#stopMovList=np.linspace(0.01,0.030,20)
#ratioVList=[0.7,0.75,0.8,0.85,0.9,1.0,1.2]
#fig=2
#
#try:
#    tem=open('dayTrade50ETF','rb')
#    dataPKL=pickle.load(tem)
#    tem.close()
#    opens=dataPKL['opens']
#    closes=dataPKL['closes']
#    highs=dataPKL['highs']
#    lows=dataPKL['lows']
#    vols=dataPKL['vols']
#    times=dataPKL['times']
#except:
#    w.start()
#    dataTem=w.wsi('510050.SH','open,high,low,close,volume',timeStart+' 09:00:00',timeEnd+' 15:01:00','periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
#    opens=dataTem.Data[0]
#    highs=dataTem.Data[1]
#    lows=dataTem.Data[2]
#    closes=dataTem.Data[3]
#    vols=dataTem.Data[4]
#    times=dataTem.Times
#    dataPKL={'opens':opens,'highs':highs,'lows':lows,'closes':closes,'vols':vols,'times':times}
#    tem=open('dayTrade50ETF','wb')
#    pickle.dump(dataPKL,tem)
#    tem.close()
#loops=len(opens)//241
#ReAll=[]
#stop=[]
#maxBar=30
#for j1 in stopAbsList:
#    for j2 in stopMovList:
#        for j3 in ratioVList:
#            stopAbs=j1
#            stopMov=j2
#            ratioV=j3
#            Re=[]
#            for i in range(loops):
#                Open=opens[i*241:(i+1)*241]
#                Close=closes[i*241:(i+1)*241]
#                High=highs[i*241:(i+1)*241]
#                Low=lows[i*241:(i+1)*241]
#                Vol=vols[i*241:(i+1)*241]
#                i2=maxBar
#                xi1=[]
#                xi2=[]
#                yi1=[]    
#                yi2=[]
#                colori=[]
#                while i2<236:
#                    maxV=np.max(Vol[i2-maxBar:i2])
#                    if Vol[i2]>maxV*ratioV and Vol[i2+1]>maxV*ratioV:
#                        priceOpen=Open[i2+3]
#                        barOpen=i2+3
#                        if round(Close[i2+2],3)>=round(Open[i2+2],3):
#                            Hold=1
#                        else:
#                            Hold=-1
#                        for i3 in range(i2+3,241):
#                            if Hold>0:
#                                if Low[i3]<=priceOpen-stopAbs:
#                                    Re.append(-stopAbs/priceOpen-0.0004)
#                                    priceClose=priceOpen-stopAbs
#                                    break
#                                elif max(High[barOpen:i3+1])-Low[i3]>=stopMov:
#                                    priceClose=max(High[barOpen:i3+1])-stopMov
#                                    Re.append(priceClose/priceOpen-1.0004)
#                                    break
#                                else:
#                                    pass
#                                    
#                                
#                            elif Hold<0:
#                                if High[i3]>=priceOpen+stopAbs:
#                                    Re.append(-stopAbs/priceOpen-0.0004)
#                                    priceClose=priceOpen+stopAbs
#                                    break
#                                if High[i3]-min(Low[barOpen:i3+1])>=stopMov:
#                                    priceClose=min(Low[barOpen:i3+1])+stopMov
#                                    Re.append(1-priceClose/priceOpen-0.0004)
#                                    break
#                            if i3==240:
#                                Re.append((Close[i3]-priceOpen)*Hold/priceOpen-0.0004)  
#                                priceClose=Close[i3]
#                        i2=i3
#                        xi1.append(barOpen)
#                        xi2.append(i3)
#                        yi1.append(priceOpen)
#                        yi2.append(priceClose)
#                        if Re[-1]>0:
#                            colori.append('purple')
#                        else:
#                            colori.append('cyan')
#                    else:
#                        i2=i2+1
#                    
#                if fig>0 and len(xi1)>=2:
#                    fig=fig-1
#                    plt.figure(figsize=(25,8))
#                    ax=plt.subplot2grid((3,1),(0,0),rowspan=2)
#                    plt.title(times[i*241].strftime('%Y-%m-%d'))
#                    candleData=np.column_stack([list(range(len(Open))),Open,High,Low,Close])
#                    mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
#                    for i2 in range(len(colori)):
#                        ax.plot([xi1[i2],xi2[i2]],[yi1[i2],yi2[i2]],colori[i2],linewidth=3)
#                    plt.xticks(range(len(Open))[::5])
#                    plt.grid()
#                    ax1=plt.subplot2grid((3,1),(2,0))
#                    ax1.bar(range(len(Vol)),Vol)
#                    plt.xticks(range(len(Open))[::5])
#                    plt.grid()
#            
#            ReAll.append(Re)
#            stop.append([stopAbs,stopMov,ratioV])
#            #plt.figure()
#            #plt.plot(np.cumsum(Re))
#indMax=np.argsort(list(map(sum,ReAll)))[-1]
#plt.figure(figsize=(25,8))
#plt.plot(np.cumsum(ReAll[indMax]))
#plt.title('stopAbs:'+str(stop[indMax][0])+';stopMove:'+str(stop[indMax][1])+';ratioV:'+str(stop[indMax][2]) )

        
      
                




#from WindPy import *
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
#import datetime,pickle,pdb
#
#
#timeStart='2016-01-01'
#timeEnd=(datetime.date.today()-timedelta(days=1)).strftime('%Y-%m-%d')
#stopAbs=0.003
#stopMov=0.008
#fig=2
#
#try:
#    tem=open('dayTrade50ETF','rb')
#    dataPKL=pickle.load(tem)
#    tem.close()
#    opens=dataPKL['opens']
#    closes=dataPKL['closes']
#    highs=dataPKL['highs']
#    lows=dataPKL['lows']
#    vols=dataPKL['vols']
#    times=dataPKL['times']
#except:
#    w.start()
#    dataTem=w.wsi('510050.SH','open,high,low,close,volume',timeStart+' 09:00:00',timeEnd+' 15:01:00','periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
#    opens=dataTem.Data[0]
#    highs=dataTem.Data[1]
#    lows=dataTem.Data[2]
#    closes=dataTem.Data[3]
#    vols=dataTem.Data[4]
#    times=dataTem.Times
#    dataPKL={'opens':opens,'highs':highs,'lows':lows,'closes':closes,'vols':vols,'times':times}
#    tem=open('dayTrade50ETF','wb')
#    pickle.dump(dataPKL,tem)
#    tem.close()
#
#loops=len(opens)//241
#Re=[]
#for i in range(loops):
#    Open=opens[i*241:(i+1)*241]
#    Close=closes[i*241:(i+1)*241]
#    High=highs[i*241:(i+1)*241]
#    Low=lows[i*241:(i+1)*241]
#    Vol=vols[i*241:(i+1)*241]
#    i2=60
#    xi1=[]
#    xi2=[]
#    yi1=[]    
#    yi2=[]
#    colori=[]
#    while i2<236:
#        maxV=max(Vol[i2-60:i2])
#        if Vol[i2]>maxV/2 and Vol[i2+1]>maxV/2:
#            priceOpen=Open[i2+3]
#            barOpen=i2+3
#            if round(Close[i2+2],3)>=round(Open[i2+2],3):
#                Hold=1
#            else:
#                Hold=-1
#            for i3 in range(i2+3,241):
#                if Hold>0:
#                    if Low[i3]<=priceOpen-stopAbs:
#                        Re.append(-stopAbs/priceOpen-0.0004)
#                        priceClose=priceOpen-stopAbs
#                        break
#                    if max(High[barOpen:i3+1])-Low[i3]>=stopMov:
#                        priceClose=max(High[barOpen:i3+1])-stopMov
#                        Re.append(priceClose/priceOpen-1.0004)
#                        break
#                else:
#                    if High[i3]>=priceOpen+stopAbs:
#                        Re.append(-stopAbs/priceOpen-0.0004)
#                        priceClose=priceOpen+stopAbs
#                        break
#                    if High[i3]-min(Low[barOpen:i3+1])>=stopMov:
#                        priceClose=min(Low[barOpen:i3+1])+stopMov
#                        Re.append(1-priceClose/priceOpen-0.0004)
#                        break
#                if i3==240:
#                    Re.append((Close[i3]-priceOpen)*Hold/priceOpen-0.0004)  
#                    priceClose=Close[i3]
#            i2=i3
#            xi1.append(barOpen)
#            xi2.append(i3)
#            yi1.append(priceOpen)
#            yi2.append(priceClose)
#            if Re[-1]>0:
#                colori.append('purple')
#            else:
#                colori.append('cyan')
#        else:
#            i2=i2+1
#        
#    if fig>0 and len(xi1)>=2:
#        fig=fig-1
#        plt.figure(figsize=(25,8))
#        ax=plt.subplot2grid((3,1),(0,0),rowspan=2)
#        plt.title(times[i*241].strftime('%Y-%m-%d'))
#        candleData=np.column_stack([list(range(len(Open))),Open,High,Low,Close])
#        mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
#        for i2 in range(len(colori)):
#            ax.plot([xi1[i2],xi2[i2]],[yi1[i2],yi2[i2]],colori[i2],linewidth=3)
##            ax.plot(xi1[i2],Low[xi1[i2]]-0.0015,colori[i2],linewidth=5)
#        plt.xticks(range(len(Open))[::5])
#        plt.grid()
#        ax1=plt.subplot2grid((3,1),(2,0))
#        ax1.bar(range(len(Vol)),Vol)
#        plt.xticks(range(len(Open))[::5])
#        plt.grid()
#
#plt.figure()
#plt.plot(np.cumsum(Re))

























