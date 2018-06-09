## -*- coding: utf-8 -*-
#"""
#Created on Wed Apr 11 15:28:14 2018
#
#@author: Administrator
#"""
#
## if 3-3-3, it is too few for difference toleration: 1 bar;please modified sth for this or test 3;
#import pymysql,time,joblib,datetime,pdb
#import matplotlib.pyplot as plt
#import matplotlib.finance as mpf
#import numpy as np
#import xgboost as xgb
#import lightgbm as lgb
#
#t0=time.time()
#reGetFeature=0 #re-calculate each feature
#reTrain=0 #whether train predict Model again;
#useXGB=1 #xgb is better than gbm much(select more good orders);if use gbm, copy more "good sample" works
#modelNow='DownUpDown' # name for saving predict model by joblib
#
#conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
#cur=conn.cursor()
#conn.select_db('pythonStocks') 
#
#fig=10
#features=[]
#profits=[]
#fetchAll=True
#    
#Lstocks=cur.execute('select number from stocks') # select name from stocks: get stocks' name;
#Number=np.insert(np.cumsum(cur.fetchall()),0,0)
#cur.execute('select name from stocks') # select name from stocks: get stocks' name;
#stocks=cur.fetchall()
#
#Lstocks=300
#t01=time.time()
#t1=t01
#for i in range(Lstocks):
#    startRow=str(Number[i])
#    endRow=str(Number[i+1]-Number[i])
#    cur.execute('select * from dataDay limit '+startRow+','+endRow)
#    dataS=np.c_[cur.fetchall()]
#    dates=dataS[0]
#    ochl=dataS[1:5]#.astype('float64')
#    opens=dataS[1]
#    closes=dataS[2]
#    highs=dataS[3]
#    lows=dataS[4]
#    vols=dataS[5]
#    exchs=dataS[6]
#    
#    L=len(opens)
#    for i2 in range(200,L):
#        for i3 in range(10,50):
#            if abs(highs[i2-i3]-max(highs[i2-i3-4:i2+1]))<0.00000001 and lows[i2]<min(lows[i2-i3-4:i2]):
#                P1=i2-i3
#                P2=np.argmin(lows[i2-i3:i2-i3//2])+P1
#                P3=np.argmax(highs[i2-i3//2:i2])+i2-i3//2
#                P4=i2
#                down1=highs[P1]-lows[P2]
#                up1=highs[P3]-lows[P2]
#                down2=highs[P3]-lows[P4]
#                downB1=P2-P1
#                upB1=P3-P2
#                downB2=P4-P3
#                if i3>25:
#                    diffBar=2
#                else:
#                    diffBar=1
#                if P4+4>=L:
#                    continue
#                if max([downB1,upB1,downB2])-min([downB1,upB1,downB2])<=diffBar and \
#                lows[P2]<=min(lows[P2:P3]) and highs[P3]>=max(highs[P2:P3]) and \
#                highs[P1]>max(highs[P1-i3:P1]) and\
#                closes[P4+1]>(highs[P3]+lows[P4])/2:#add all down is less than 0.5
#                    fig=plt.figure(figsize=(10,6))
#                    ax=fig.add_axes([0.1,0.3,0.8,0.6])   
#                    baseBar=i2-2*i3;lastBar=min(L,i2+2*i3)
#                    Lbars=lastBar-baseBar
#                    basex=range(Lbars)
#                    bollUp=[]
#                    bollMiddle=[]
#                    bollDown=[]
#                    for i4 in range(baseBar,lastBar):
#                        avg=closes[i4-20:i4+1].mean()
#                        std=closes[i4-20:i4+1].std()
#                        bollUp.append(avg+1.7*std)
#                        bollMiddle.append(avg)
#                        bollDown.append(avg-1.7*std)
#                    ax.plot(basex,bollUp,'r--',basex,bollMiddle,'b--',basex,bollDown,'r--')
#                    ax.plot([P1-baseBar,P2-baseBar,P3-baseBar,P4-baseBar],[highs[P1],lows[P2],highs[P3],lows[P4]],color='k')
#                    ax.text(P1-baseBar,highs[P1],round(down1/up1,3))
#                    ax.text(P3-baseBar,highs[P3],round(down2/up1,3))
#                    candleData=np.column_stack([basex,opens[baseBar:lastBar],highs[baseBar:lastBar],lows[baseBar:lastBar],closes[baseBar:lastBar]])
#                    mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
#                    ax.set_xticks(range(0,Lbars,3))
#                    ax.grid()
#                    plt.title(stocks[i][0]+':'+datetime.datetime.strftime(dates[i2],'%Y-%m-%d'))
#                    
#                    ax1=fig.add_axes([0.1,0.1,0.8,0.2])
#                    vol=vols[baseBar:lastBar]
#                    ax1.bar(basex,vol)
#                    ax1.set_xticks(range(0,Lbars,3))
#                    ax1.grid()                   
#                    break # stop search more patten
#                    
#    

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:28:14 2018

@author: Administrator
"""

# if 3-3-3, it is too few for difference toleration: 1 bar;please modified sth for this or test 3;
import pymysql,time,joblib,datetime,pdb
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier

t0=time.time()
reGetFeature=0 #re-calculate each feature
reTrain=0 #whether train predict Model again;
useXGB=1 #xgb is better than gbm much(select more good orders);if use gbm, copy more "good sample" works
modelNow='DownUpDown' # name for saving predict model by joblib

conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
cur=conn.cursor()
conn.select_db('pythonStocks') 

fig=1
features=[]
profits=[]
fetchAll=True
    
Lstocks=cur.execute('select number from stocks') # select name from stocks: get stocks' name;
Number=np.insert(np.cumsum(cur.fetchall()),0,0)
cur.execute('select name from stocks') # select name from stocks: get stocks' name;
stocks=cur.fetchall()

Lstocks=10
#cur.execute('select * from dataDay')
#dataAll=np.c_[cur.fetchall()]

t01=time.time()
t1=t01
features=[]
labels=[]
for i in range(Lstocks):
    startRow=str(Number[i])
    endRow=str(Number[i+1]-Number[i])
    cur.execute('select * from dataDay limit '+startRow+','+endRow)
    dataS=np.c_[cur.fetchall()]
    dates=dataS[0]
    ochl=dataS[1:5]#.astype('float64')
    opens=dataS[1]
    closes=dataS[2]
    highs=dataS[3]
    lows=dataS[4]
    vols=dataS[5]
    exchs=dataS[6]
#    dates=dataAll[0][Number[i]:Number[i+1]]
#    opens=dataAll[1][Number[i]:Number[i+1]]
#    closes=dataAll[2][Number[i]:Number[i+1]]
#    highs=dataAll[3][Number[i]:Number[i+1]]
#    lows=dataAll[4][Number[i]:Number[i+1]]
#    vols=dataAll[5][Number[i]:Number[i+1]]
#    exchs=dataAll[6][Number[i]:Number[i+1]]
#    print(stocks[i][0]+":"+str(i))
    
    L=len(opens)
    for i2 in range(50,L):
        if lows[i2]<min(lows[i2-4:i2]) and lows[i2-8]<=min(lows[i2-12:i2-4]) and \
        abs(lows[i2]-lows[i2-8])/lows[i2]<0.01 and highs[i2-4]>=max(highs[i2-8:i2]) and\
        min(highs[i2-8:i2]-lows[i2-8:i2])>0.0000001:
            if i2+8>=L:
                continue
            baseP=closes[i2];baseV=vols[i2]
            backBar=8
            Ftmp=np.r_[highs[i2-backBar:i2]/baseP,lows[i2-backBar:i2]/baseP,opens[i2-backBar:i2]/baseP,closes[i2-backBar:i2]/baseP,vols[i2-backBar:i2]/baseV]
            features.append(Ftmp.tolist())
            if max(highs[i2+1:i2+8])>highs[i2-4] and min(lows[i2+1:i2+8])/lows[i2]>0.99:
                labels.append(1)
            else:
                labels.append(0)
            
            if fig:
                P1=i2-8
                P2=i2-4
                P3=i2
                fig=plt.figure(figsize=(10,6))
                ax=fig.add_axes([0.1,0.3,0.8,0.6])   
                baseBar=i2-16;lastBar=min(L,i2+12)
                Lbars=lastBar-baseBar
                basex=range(Lbars)
                bollUp=[]
                bollMiddle=[]
                bollDown=[]
                for i3 in range(baseBar,lastBar):
                    avg=closes[i3-20:i3+1].mean()
                    std=closes[i3-20:i3+1].std()
                    bollUp.append(avg+1.7*std)
                    bollMiddle.append(avg)
                    bollDown.append(avg-1.7*std)
                ax.plot(basex,bollUp,'r--',basex,bollMiddle,'b--',basex,bollDown,'r--')
                ax.plot([P1-baseBar,P2-baseBar,P3-baseBar],[lows[P1],highs[P2],lows[P3]],color='k')
                candleData=np.column_stack([basex,opens[baseBar:lastBar],highs[baseBar:lastBar],lows[baseBar:lastBar],closes[baseBar:lastBar]])
                mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
                ax.set_xticks(range(0,Lbars,3))
                ax.grid()
                plt.title(stocks[i][0]+':'+datetime.datetime.strftime(dates[i2],'%Y-%m-%d'))
                
                ax1=fig.add_axes([0.1,0.1,0.8,0.2])
                vol=vols[baseBar:lastBar]
                ax1.bar(basex,vol)
                ax1.set_xticks(range(0,Lbars,3))
                ax1.grid()                  
Features=np.array(features);Labels=np.array(labels)
tmp=Labels>0
winF=Features[tmp]
lossF=Features[~ tmp]
winL=sum(tmp)
lossFS=lossF[np.random.choice(len(lossF),winL,replace=False)]
featuresS=np.r_[winF,lossFS];labelsS=np.ones(len(featuresS));labelsS[winL:]=0
tmp=np.random.choice(len(labelsS),len(labelsS),replace=True)
featuresS=featuresS[tmp];labelsS=labelsS[tmp]
xTrain=featuresS[:1200];yTrain=labelsS[:1200]
xTest=featuresS[1200:];yTest=labelsS[1200:]

#pca = PCA(0.85)
#xTrain=pca.fit_transform(xTrain)
#xTest=pca.transform(xTest)
#clf=MLPClassifier(solver='lbfgs',max_iter=30000,hidden_layer_sizes=(100,55,20,10,5),activation='tanh')
#clf.fit(xTrain,yTrain)
#pred=clf.predict(xTest)

clf=SVC(C=12000, kernel='rbf', gamma=0.2)
clf.fit(xTrain, yTrain)
pred=clf.predict(xTest)
print(sum(pred>0)/len(pred))
tmp=pred>0
print(sum(yTest[tmp]<1)/sum(tmp))

