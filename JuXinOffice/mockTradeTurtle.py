# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:45:15 2017

@author: Administrator
"""

from WindPy import *
import numpy as np
import time,datetime,pdb,pickle

objTrade=['RB.SHF','I.DCE']
contractMulti=[10,100]
minTick=[1,0.5]
setTime='23:30:00' # such as '01:10:25' and so on

w.start()
tem=[]
for i in range(len(minTick)):
    tem.append(objTrade[i][-3:].upper())
tem=w.tlogon('0000', '0', 'W115294100302', '*********', tem) # CZC:郑商所；SHF:上期所；DCE:大商所；CFE：中金所
logId=tem.Data[0][0] #should chech whether is ok when logId switch;
today=time.strftime('%Y-%m-%d')
tem=np.zeros(len(objTrade))
hands=tem;stopLoss=tem.copy()
up20=tem.copy();down20=tem.copy();up10=tem.copy();down10=tem.copy();ATR=tem.copy();openPrice=tem.copy();holds=tem.copy()

tem=int(time.strftime('%H'))
if tem>=15:
    timeEnd=time.strftime('%Y-%m-%d')
else:
    timeEnd=(datetime.date.today()-timedelta(days=1)).strftime('%Y-%m-%d')    
for i in range(len(objTrade)):
    price20=w.wsd(objTrade[i],'high,low','ED-19TD',timeEnd).Data
    up20[i]=max(price20[0])
    down20[i]=min(price20[1])
    up10[i]=max(price20[0][:10])
    down10[i]=min(price20[1][:10])
try:
    tem=open('mockTrade','rb')
    datatem=pickle.load(tem)
    tem.close()
    holds=datatem['holds']
    stopLoss=datatem['stopLoss']
    openPrice=datatem['openPrice']
    ATR=datatem['ATR']
    hands=datatem['hands']
except:
    print('not find MockTrade file.')    
    
#define the callback function
def myCallback(indata):
    global objTrade,hands,stopLoss,up20,down20,up10,down10,openPrice,ATR,holds,logId,today,timex  
    if indata.ErrorCode!=0:
        print('error code:'+str(indata.ErrorCode)+'\n')
        return()
    loops=len(objTrade)
    now=time.localtime(time.time())
    if time.strftime('%H-%M',now)=='15-00':
        for i in range(loops):
            price20=w.wsd(objTrade[i],'high,low','ED-19TD',time.strftime('%Y-%m-%d',now)).Data
            up20[i]=max(price20[0])
            down20[i]=min(price20[1])
            up10[i]=max(price20[0][:10])
            down10[i]=min(price20[1][:10])
    
    Codes=indata.Codes
    for i in range(len(Codes)):
        obji=objTrade.index(Codes[i])
        if holds[obji]==0:
            print(objTrade[obji],up20[obji]-indata.Data[0][i],indata.Data[0][i]-down20[obji])
            if indata.Data[0][i] > up20[obji]:
                tem=w.wsd(objTrade[obji],'high,low,close','ED-2TD',today)
                high_1=tem.Data[0][1];low_1=tem.Data[1][1];close_2=tem.Data[2][0]                 
                ATRtem=max([high_1-low_1,abs(high_1-close_2),abs(low_1-close_2)])
                tem=1000000//(100*contractMulti[obji]*ATRtem)         
                w.torder(objTrade[obji], 'Buy', indata.Data[0][i]+minTick[obji], tem, 'OrderType=LMT;LogonID='+str(logId))
                hands[obji]=tem
                openPrice[obji]=indata.Data[0][i]+minTick[obji]
                stopLoss[obji]=openPrice[obji]-2*ATRtem
                holds[obji]=1
                ATR[obji]=ATRtem
                print('buy '+objTrade[obji]+';hands: '+hands[obji])
            if indata.Data[0][i] < down20[obji]:
                tem=w.wsd(objTrade[obji],'high,low,close','ED-2TD',today)
                high_1=tem.Data[0][1];low_1=tem.Data[1][1];close_2=tem.Data[2][0]
                ATRtem=max([high_1-low_1,abs(high_1-close_2),abs(low_1-close_2)])
                tem=1000000//(100*contractMulti[obji]*ATRtem)        
                w.torder(objTrade[obji], 'Sell', indata.Data[0][i]-minTick[obji], tem, 'OrderType=LMT;LogonID='+str(logId))
                hands[obji]=tem
                openPrice[obji]=indata.Data[0][i]-minTick[obji]
                stopLoss[obji]=openPrice[obji]+2*ATRtem
                holds[obji]=-1
                ATR[obji]=ATRtem
                print('sell '+objTrade[obji]+';hands: '+hands[obji])
        else:
            diffTem=(indata.Data[0][i]-openPrice[obji])*holds[obji]
            if diffTem>ATR[obji]/2 and abs(holds[obji])<=4:
                if holds[obji]>0:
                    w.torder(objTrade[obji], 'Buy', indata.Data[0][i]+minTick[obji], hands[obji], 'OrderType=LMT;LogonID='+str(logId))
                    openPrice[obji]=indata.Data[0][i]+minTick[obji]
                    stopLoss[obji]=openPrice[obji]-2*ATR[obji]
                    holds[obji]=holds[obji]+1
                    print('long another '+objTrade[obji])
                else:
                    w.torder(objTrade[obji], 'Sell', indata.Data[0][i]-minTick[obji], hands[obji], 'OrderType=LMT;LogonID='+str(logId))
                    openPrice[obji]=indata.Data[0][i]-minTick[obji]
                    stopLoss[obji]=openPrice[obji]+2*ATR[obji]
                    holds[obji]=holds[obji]-1
                    print('short another '+objTrade[obji])
                
            if (indata.Data[0][i]-openPrice[obji])*holds[obji]<0 or \
            (holds[obji]>0 and indata.Data[0][i]<up10[obji]) or \
            (holds[obji]<0 and indata.Data[0][i]>up10[obji]):
                dataTem=w.tquery('Position', 'LogonId='+str(logId))
                indTem=dataTem.Data[0].index(Codes[i])
                handTem=dataTem.Data[6][indTem]
                tradeSide=dataTem.Data[4][indTem]
                if tradeSide=='Buy':
                    tradeSide=='Sell'
                    tem=-1
                else:
                    tradeSide=='Buy'
                    tem=1
                w.torder(objTrade[obji], tradeSide, indata.Data[0][i]+tem*minTick[obji], handTem, 'OrderType=LMT;LogonID='+str(logId))
                openPrice[obji]=0
                stopLoss[obji]=0
                holds[obji]=0        
    
    if time.strftime('%H:%M:%S')==setTime and holds.sum():
        datatem={'holds':holds,'stopLoss':stopLoss,'openPrice':openPrice,'ATR':ATR,'hands':hands}
        tem=open('mockTrade','wb')
        pickle.dump(datatem,tem)
        tem.close() 
        
            
#    for i in range(loops):
#        holdi=holds[i];handi=hands[i];stopLossi=stopLoss[i];up20i=up20[i];down20i=down20[i];
#        up10i=up10[i];down10i=down10[i];ATRi=ATR[i];openPricei=openPrice[i]
#        
#        if holdi==0:


##    global begintime
#    lastvalue =""
#    for k in range(0,len(indata.Fields)):
#         if(indata.Fields[k] == "RT_TIME"):
#            begintime = indata.Data[k][0]
#         if(indata.Fields[k] == "RT_LAST"):
#            lastvalue = str(indata.Data[k][0])
#
#    string = str(begintime) + " " + lastvalue +"\n"
#    pf.writelines(string)
#    tem=w.wsd('RB.SHF','close','ED-4TD','2017/9/14')
#    print(tem.Data)

    #应该在w.cancelRequest后调用pf.close()
    #pf.close();

data=w.wsq(','.join(objTrade),"rt_last",func=myCallback)
#w.cancelRequest(data.RequestID)
#pf.close()









