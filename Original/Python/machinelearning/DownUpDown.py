# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:28:14 2018

@author: Administrator
"""

#import tushare as ts
import pymysql,time
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
import xgboost as xgb

t0=time.time()
reGetFeature=True

conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
cur=conn.cursor()
conn.select_db('pythonStocks') 
if reGetFeature:
    fig=0
    features=[]
    profits=[]
    fetchAll=True
        
    Lstocks=cur.execute('select number from stocks') # select name from stocks: get stocks' name;
    Number=np.insert(np.cumsum(cur.fetchall()),0,0)
    cur.execute('select name from stocks') # select name from stocks: get stocks' name;
    stocks=cur.fetchall()
    #cur.execute('select * from dataDay') #'select * from dataDay limit '
    #dataAll=np.column_stack(cur.fetchall())
    if fetchAll:
        cur.execute('select * from dataDay')
        dataAll=np.c_[cur.fetchall()]
    else:
        Lstocks=10
    t01=time.time()
    t1=t01
    for stockI in range(Lstocks):
        if fetchAll:
            date=dataAll[0][Number[stockI]:Number[stockI+1]]
            opens=dataAll[1][Number[stockI]:Number[stockI+1]]
            closes=dataAll[2][Number[stockI]:Number[stockI+1]]
            highs=dataAll[3][Number[stockI]:Number[stockI+1]]
            lows=dataAll[4][Number[stockI]:Number[stockI+1]]
            vols=dataAll[5][Number[stockI]:Number[stockI+1]]
            exchs=dataAll[6][Number[stockI]:Number[stockI+1]]
        else:
            startRow=str(Number[stockI])
            endRow=str(Number[stockI+1]-Number[stockI])
            cur.execute('select * from dataDay limit '+startRow+','+endRow)
            dataS=np.c_[cur.fetchall()]
            date=dataS[0]
            ochl=dataS[1:5]#.astype('float64')
            opens=dataS[1]
            closes=dataS[2]
            highs=dataS[3]
            lows=dataS[4]
            vols=dataS[5]
            exchs=dataS[6]
        
        L=len(opens)
        for i in range(10,L):
            for i2 in range(3,10):
                if i-3*i2-5<0:
                    break
    #            if closes[i]>opens[i]:
    #                continue
                
                if abs(max(highs[i-3*i2-1:i-3*i2+2])-max(highs[i-3*i2-5:i+1]))<0.00000001 and \
                abs(min(lows[i-3*i2:i-i2+2])-min(lows[i-2*i2-1:i-2*i2+2]))<0.00000001 and \
                abs(max(highs[i-2*i2:i+1])-max(highs[i-i2-1:i-i2+2]))<0.00000001 and \
                lows[i]<min(lows[i-i2-1:i]) and \
                min(highs[i-3*i2-5:i+1]-lows[i-3*i2-5:i+1])>0.0000001:
                    P1=np.argmax(highs[i-3*i2-5:i+1]) #index 0 is i-3*i2-5
                    P2=np.argmin(lows[i-2*i2-1:i-2*i2+2])+i2+4
                    P3=np.argmax(highs[i-i2-1:i-i2+2])+2*i2+4
                    P4=3*i2+5
                    down1=P2-P1
                    up=P3-P2
                    down2=P4-P3
                    if max([down1,up,down2])-min([down1,up,down2])<2:
                        if i+i2>L-1: #if this profit can't be caculated by future bars;
                            break
                        baseI=i-3*i2-5
                        baseL=highs[baseI+P1]-lows[baseI+P2]
                        try:
                            baseE=sum(exchs[baseI+P1-i2:baseI+P1])
                            if baseE<1:
                                continue
                        except:
                            continue                            
                        features.append([(highs[baseI+P3]-lows[baseI+P2])/baseL,(highs[baseI+P3]-lows[baseI+P4])/baseL,\
                                         sum(exchs[baseI+P1+1:baseI+P2+1])/baseE,sum(exchs[baseI+P2+1:baseI+P3+1])/baseE,\
                                         sum(exchs[baseI+P3+1:baseI+P4+1])/baseE])
                        stopL=lows[i]
                        if min(lows[i+1:i+i2+1])<stopL:
                            tmp=stopL/closes[i]-1.004
                        else:
                            tmp=closes[i+i2]/closes[i]-1.004
                        profits.append(tmp)
        
                        if fig>0 and np.random.rand(1)>0.5:
                            fig-=1
                            plt.figure(figsize=(10,6))
                            ax=plt.subplot()
                            candleData=np.column_stack([range(P4+1),opens[baseI:i+1],highs[baseI:i+1],lows[baseI:i+1],closes[baseI:i+1]])
                            mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
                            plt.plot([P1,P2,P3,P4],[highs[baseI+P1],lows[baseI+P2],highs[baseI+P3],lows[baseI+P4]],color='k')
                            plt.title(stocks[stockI])
                            plt.grid()
        t2=time.time()
        ratioStocks=(stockI+1)/Lstocks    
        print(stocks[stockI][0]+':'+str(round(100*ratioStocks,2))+'%,and need more time:{} minutes'.format(round((t2-t1)*(1/ratioStocks-1)/60,2)))
    
    cur.execute('drop table if exists DownUpDown')
    cur.execute('create table DownUpDown(ind0 float,ind1 float,ind2 float,ind3 float,ind4 float,ind5 float)')
    tmp=np.column_stack([profits,features])
    cur.executemany('insert into DownUpDown values(%s,%s,%s,%s,%s,%s)', tmp.tolist())
    conn.commit()
    features=np.array(features)
    profits=np.array(profits)
else:
    cur.execute('select * from DownUpDown')
    tmp=np.c_[cur.fetchall()]
    profits=tmp[0]
    features=tmp[1:,:].T

cur.close()
conn.close()
t2=time.time()

Lprofits=len(profits)
tmp=np.random.choice(Lprofits,Lprofits,replace=True)
features=features[tmp,:]
profits=profits[tmp]
Ls=Lprofits*3//5
Ftrain=features[:Ls];Ptrain=profits[:Ls]
Ftest=features[Ls:];Ptest=profits[Ls:]

#tmp=Ptrain>0
#Ftrain=np.r_[Ftrain,Ftrain[tmp],Ftrain[tmp],Ftrain[tmp]]
#Ptrain=np.r_[Ptrain,Ptrain[tmp],Ptrain[tmp],Ptrain[tmp]]

tmp=len(Ptrain)
tmp=np.random.choice(tmp,tmp,replace=False)
Ftrain=Ftrain[tmp]
Ptrain=Ptrain[tmp]
tmp=len(Ptrain)//8
data_test=xgb.DMatrix(data=Ftrain[:tmp,:],label=Ptrain[:tmp]>0)
data_train=xgb.DMatrix(data=Ftrain[tmp:,:],label=Ptrain[tmp:]>0)
watch_list={(data_test,'eval'),(data_train,'train')}
param={'max_depth':3,'eta':0.03,'early_stopping_rounds':3,'silent':0,'objective':'multi:softmax','num_class':2}
XGB=xgb.train(param,data_train,num_boost_round=20000,evals=watch_list)
#XGB=xgb.train(param,data_train,num_boost_round=20000)
ProfitP=XGB.predict(xgb.DMatrix(data=Ftest))
Pselect=Ptest[ProfitP>0]
winRatio=sum(Pselect>0)/len(Pselect)
IC=np.mean(Pselect)/np.std(Pselect)
maxDown=0
Pcumsum=Pselect.cumsum()
for i in range(1,len(Pselect)):
    tmp=max(Pcumsum[:i])-Pcumsum[i]
    if tmp>maxDown:
        maxDown=tmp
plt.plot(Pcumsum)
plt.title('winRatio:{}%,IC:{},maxDown:{}%'.format(round(winRatio*100,2),round(IC,2),round(maxDown*100,2)))
plt.grid()

t3=time.time()
if reGetFeature:
    print('Preparing for Data consumes time {} minutes'.format(round((t01-t0)/60,2)))
    print('Extracting features and profits consumes time {} minutes'.format(round((t2-t01)/60,2)))
else:
    print('Extracting features and profits consumes time {} minutes'.format(round((t2-t0)/60,2)))
print('xgb training consumes all time {} minutes'.format(round((t3-t2)/60,2)))














