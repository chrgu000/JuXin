# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:46:01 2017

@author: Administrator
"""

from hmmlearn.hmm import GaussianHMM
from seqlearn.perceptron import StructuredPerceptron
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap
from matplotlib.pylab import date2num
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
import pandas as pd
import scipy.io as sio
import joblib, warnings,pymysql,time

x1=time.clock()
warnings.filterwarnings("ignore")
nameDB='Up2Down2'
saveData='D:\\Trade\\joblib\\'+nameDB

def plot_decision_regions(X,y,classifier,resolution=0.02):
    markers=('s','x','o','^','v')
    colors=('red','blue','lightgreen','gray','cyan')
    cmap=ListedColormap(colors[:len(np.unique(y))])
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                         np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)

def hmmTestAll(Xraw,Reraw,figStart): # figStart: how many figs to show 0 means show all and Xcol mean show one (in all)
    Xshape=Xraw.shape
    Xrow=Xshape[0]
    Xcol=Xshape[1]
    if figStart!=Xcol:
        Xraw,X0,Reraw,y0=train_test_split(Xraw,np.array(Reraw),test_size=0.0)
    for lp in range(figStart,Xcol+1):
        if lp<Xcol:
            X=Xraw[:,lp]
            figTitle=str(lp)
        else:
            X=Xraw
            figTitle='All'
        trainSample=30000
        if Xrow<trainSample:
            Xtrain=X[:Xrow//2]
            Xtest=X[Xrow//2:]
            Retrain=Reraw[:Xrow//2]
            Retest=Reraw[Xrow//2:]
        else:
            Xtrain=X[:trainSample]
            Xtest=X[trainSample:]    
            Retrain=Reraw[:trainSample]  
            Retest=Reraw[trainSample:]
        if figStart==Xcol:
            Xtest=X
            Retest=Reraw
            figTitle='AllSelected'

        hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=10000).fit(np.row_stack(Xtrain)) #spherical,diag,full,tied 
        joblib.dump(hmm,saveData+figTitle)
        
#        for i in range(2):
        for i in range(1,2):
            
            if i==0:
                Xtem=Xtrain
                Retem=Retrain
            else:
                Xtem=Xtest
                Retem=Retest
                
            flag=hmm.predict(np.row_stack(Xtem))
            plt.figure(figsize=(15,8))
            xi=[]
            yi=[]
            for i2 in range(hmm.n_components):
                state=(flag==i2)
                ReT=Retem[state]
                ReTcs=ReT.cumsum()
                LT=len(ReT)
                if LT<2:
                    continue
                maxDraw=0
                maxDrawi=0
                maxDrawValue=0
                i2High=0
                for i3 in range(LT):
                    if ReTcs[i3]>i2High:
                        i2High=ReTcs[i3]
                    drawT=i2High-ReTcs[i3]
                    if maxDraw<drawT:
                        maxDraw=drawT
                        maxDrawi=i3
                        maxDrawValue=ReTcs[i3]
                xi.append(maxDrawi)
                yi.append(maxDrawValue)  
                plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                         %(i2,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
            plt.plot(xi,yi,'r*')
            plt.title(figTitle,fontsize=16)
    #        plt.legend(loc='upper',bbox_to_anchor=(0.0,1.0),ncol=1,fancybox=True,shadow=True)
            plt.legend(loc='upper left')
            plt.grid(1)
    if figStart==Xcol:
        return flag
       

def hmmTestCertain(Matrix,Re,flagSelected):
    X=np.row_stack(Matrix)  
    def hmmTCi(paraList): #Nind -- which indicator; flaNot -- not which flag for this indicator;
        Nind=[]
        flagNot=[]
        for i in range(len(paraList)):
            Nind.append(paraList[i][0])
            flagNot.append(paraList[i][1])            
        flag=np.ones(len(X))>0
        for i2 in range(len(Nind)):    
            hmm=joblib.load(saveData+str(Nind[i2]))
            flagTem=hmm.predict(np.row_stack(X[:,Nind[i2]]))
            for i in range(len(flagNot[i2])):
                    flag=flag*(flagTem!=flagNot[i2][i])       
        return flag
    
    flag=hmmTCi(flagSelected)

    ReT=Re[flag]
    ReTcs=ReT.cumsum()
    LT=len(ReT)
    maxDraw=0
    maxDrawi=0
    maxDrawValue=0
    i2High=0
    for i2 in range(LT):
        if ReTcs[i2]>i2High:
            i2High=ReTcs[i2]
        drawT=i2High-ReTcs[i2]
        if maxDraw<drawT:
            maxDraw=drawT
            maxDrawi=i2
            maxDrawValue=ReTcs[i2]
    plt.figure(figsize=(15,8))
    plt.plot(range(LT),ReTcs,label='latent_state: %s;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
             %('Selected',LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
    plt.plot(maxDrawi,maxDrawValue,'r*')
    plt.legend(loc='upper left')
    plt.grid(1) 
    return flag

def seqTrain(Matrix,Re,figTitle):
    X = np.row_stack(Matrix)
    X_train,X_test,y_train,y_test=train_test_split(X,Re,test_size=0.5)
#    X_train=X;X_test=X;y_train=Re;y_test=Re;

    y_trainLabel=np.ones(len(y_train))*3
    diff=0.005
    indTem=y_train<-diff
    y_trainLabel[indTem]=1
    indTem=y_train>diff#indTem=(y_train>=-0.01)*(y_train<=0.01)
    y_trainLabel[indTem]=2
    indTem=y_trainLabel<3
    y_trainLabel=y_trainLabel[indTem]
    X_train=X_train[indTem,:]

    y_testLabel=np.ones(len(y_test))*2
    indTem=y_test<0.0
    y_testLabel[indTem]=1

#    y_trainLabel=np.ones(len(y_train))*3
#    indTem=y_train<-0.01
#    y_trainLabel[indTem]=1
#    indTem=(y_train>=-0.01)*(y_train<=0.01)
#    y_trainLabel[indTem]=2
#    y_testLabel=np.ones(len(y_test))*3
#    indTem=y_test<-0.01
#    y_testLabel[indTem]=1
#    indTem=(y_test>=-0.01)*(y_test<=0.01)
#    y_testLabel[indTem]=2
    
#    seq=StructuredPerceptron()
#    seq.fit(X_train.tolist(),y_trainLabel.tolist(),[len(y_trainLabel),])
#    #joblib.dump(hmm,'HMMTest')
#    y_pred=seq.predict(X_test.tolist(),[len(y_test)])
    svm=SVC(kernel='rbf',random_state=0,gamma=0.10,C=1000000)
    svm.fit(X_train,y_trainLabel)
    y_pred=svm.predict(X_test)

    print (figTitle+'-accuracy:%.3f%%' %( (y_testLabel==y_pred).sum()*100/float(len(y_test)) ))
    
    yU=np.unique(y_pred)
    plt.figure(figsize=(15,8))
    xi=[]
    yi=[]
    for i in range(len(yU)):
        state=(y_pred==yU[i])
        ReT=y_test[state]
        ReTcs=ReT.cumsum()
        LT=len(ReT)
        if LT<2:
            continue
        maxDraw=0
        maxDrawi=0
        maxDrawValue=0
        i2High=0
        for i2 in range(LT):
            if ReTcs[i2]>i2High:
                i2High=ReTcs[i2]
            drawT=i2High-ReTcs[i2]
            if maxDraw<drawT:
                maxDraw=drawT
                maxDrawi=i2
                maxDrawValue=ReTcs[i2]
        xi.append(maxDrawi)
        yi.append(maxDrawValue)  
        plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.2f%%;'\
                 %(i,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
    plt.plot(xi,yi,'r*')
    plt.title(figTitle)
    plt.legend()
    plt.grid(1)

def PCAtest(Matrix,Re):
    figTitle='test'
    pca=PCA(n_components=12)
    X_train,X_test,y_train,y_test=train_test_split(Matrix,Re,test_size=0.5)
    y_trainLabel=np.ones(len(y_train))*3
    indTem=y_train<0
    y_trainLabel[indTem]=1
#    indTem=(y_train>=-0.01)*(y_train<=0.01)
#    y_trainLabel[indTem]=2
    y_testLabel=np.ones(len(y_test))*3
    indTem=y_test<0
    y_testLabel[indTem]=1
#    indTem=(y_test>=-0.01)*(y_test<=0.01)
#    y_testLabel[indTem]=2
    svm=SVC(kernel='rbf',random_state=0,gamma=0.10,C=1000000)
    X_train_pca=pca.fit_transform(X_train)
    X_test_pca=pca.transform(X_test)
    svm.fit(X_train_pca,y_trainLabel)
#    plot_decision_regions(X_train_pca,y_trainLabel,classifier=svm)   
    
    y_pred=svm.predict(X_test_pca)
    print (figTitle+'-accuracy:%.3f%%' %( (y_testLabel==y_pred).sum()*100/float(len(y_test)) ))
    
    yU=np.unique(y_pred)
    plt.figure(figsize=(15,8))
    xi=[]
    yi=[]
    for i in range(len(yU)):
        state=(y_pred==yU[i])
        ReT=y_test[state]
        ReTcs=ReT.cumsum()
        LT=len(ReT)
        if LT<2:
            continue
        maxDraw=0
        maxDrawi=0
        maxDrawValue=0
        i2High=0
        for i2 in range(LT):
            if ReTcs[i2]>i2High:
                i2High=ReTcs[i2]
            drawT=i2High-ReTcs[i2]
            if maxDraw<drawT:
                maxDraw=drawT
                maxDrawi=i2
                maxDrawValue=ReTcs[i2]
        xi.append(maxDrawi)
        yi.append(maxDrawValue)  
        plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.2f%%;'\
                 %(i,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
    plt.plot(xi,yi,'r*')
    plt.title(figTitle)
    plt.legend()
    plt.grid(1)

def sortStatastic(sorts,Re,Title):
    sorts=np.array(sorts)
    sortsU=np.unique(sorts)
    plt.figure(figsize=(15,8))
    ax=plt.subplot(1,1,1)
    xi=[]
    yi=[]
    profitP=[]
    for i in range(len(sortsU)):
        state=(sorts==sortsU[i])
        ReT=Re[state]
        ReTcs=ReT.cumsum()
        LT=len(ReT)
        if LT<2:
            continue
        maxDraw=0
        maxDrawi=0
        maxDrawValue=0
        i2High=0
        for i2 in range(LT):
            if ReTcs[i2]>i2High:
                i2High=ReTcs[i2]
            drawT=i2High-ReTcs[i2]
            if maxDraw<drawT:
                maxDraw=drawT
                maxDrawi=i2
                maxDrawValue=ReTcs[i2]
        xi.append(maxDrawi)
        yi.append(maxDrawValue)  
        profitP.append(ReTcs[-1]/LT*100)
        ax.plot(range(LT),ReTcs,label='latent_state %s;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.2f%%;'\
                 %(sortsU[i],LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
    ax.plot(xi,yi,'r*')
    handles, labels = ax.get_legend_handles_labels()
    tem=np.argsort(profitP)[::-1]
    ax.legend(np.array(handles)[tem],np.array(labels)[tem],loc='upper left', bbox_to_anchor=(1.0, 1.0), ncol=1, fancybox=True, shadow=True)
    plt.title(Title)
    plt.grid(1)
    

sw0=0 # get dataset for the model and test all for the first time;
sw1=0 # test selected figures;
sw2=0 # show one figure with one line after delete some bad type (should be done by hand)
sw3=1 # show one figure with different line of hmm sort according to sw2's selected and then show many features according to different date/time;
sw3_1=0 # show many figures and each one is sorted according to different date/time; 
sw4=0 # train by seq   
sw5=0 # PCA

if sw0:   
    fig=10
    conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
    cur=conn.cursor()
    cur.execute('create database if not exists '+nameDB) # create database;        
    conn.select_db('pythonStocks')     
    Lstocks=cur.execute('select number from stocks') # select name from stocks: get stocks' name;
    Number=np.insert(np.cumsum(cur.fetchall()),0,0)
    cur.execute('select name from stocks') # select name from stocks: get stocks' name;
    stocks=cur.fetchall()
    cur.execute('select * from dataDay') #'select * from dataDay limit '
    dataAll=np.column_stack(cur.fetchall())

    Re=[]
    dateAll=[]
    Matrix=[]
    for i in range(Lstocks):
        print('%s:%d' %(stocks[i][0],i+1),end=' ',flush=True) #print(i, sep=' ', end=' ', flush=True)
        startT=Number[i]
        endT=Number[i+1]
        dates=dataAll[0][startT:endT]
        opens=dataAll[1][startT:endT]
        closes=dataAll[2][startT:endT]
        highs=dataAll[3][startT:endT]
        lows=dataAll[4][startT:endT]
        vols=dataAll[5][startT:endT]
        turns=dataAll[6][startT:endT]
        
        Lt=len(opens)
        if Lt<20:
            continue
#        maN=np.zeros(Lt)
#        ma10=np.zeros(Lt)
#        for i2 in range(10,Lt):
#            maN[i2]=np.mean(closes[i2-3:i2+1])
#            ma10[i2]=np.mean(closes[i2-10:i2+1])
        for i2 in range(15,Lt-3):
            if lows[i2-3]<=min(lows[i2-5:i2+1]) and highs[i2-2]>highs[i2-3] and highs[i2-1]>highs[i2] and lows[i2-1]>lows[i2] and \
            highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2] and closes[i2]/closes[i2-1]<1.095: #vols[i2-2:i2].min()>vols[[i2-3,i2]].max() and 
                if closes[i2+1]>closes[i2]:
                    Re.append(closes[i2+2]/closes[i2]-1)
                else:
                    Re.append(closes[i2+1]/closes[i2]-1)
                dateAll.append(dates[i2])
                if max(closes[i2-4:i2+1])>max(closes[i2-9:i2-4]) and min(closes[i2-4:i2+1])>min(closes[i2-9:i2-4]):
                    ud5=1
                elif max(closes[i2-4:i2+1])<max(closes[i2-9:i2-4]) and min(closes[i2-4:i2+1])<min(closes[i2-9:i2-4]):
                    ud5=-1
                else:
                    ud5=0
                if max(highs[i2-6:i2+1])>max(highs[i2-13:i2-6]) and min(lows[i2-6:i2+1])>min(lows[i2-13:i2-6]):
                    ud_7=1
                elif max(highs[i2-6:i2+1])<max(highs[i2-13:i2-6]) and min(lows[i2-6:i2+1])<min(lows[i2-13:i2-6]):
                    ud_7=-1
                else:
                    ud_7=0
                                       
                tem=[ ud5,vols[i2]/vols[i2-2],ud_7,pd.DataFrame([lows[i2-3],opens[i2-3],closes[i2-3],highs[i2-3]])[0].corr(pd.DataFrame([lows[i2],closes[i2],opens[i2],highs[i2]])[0]),\
                    vols[i2]/vols[i2-3],vols[i2]/vols[i2-1],vols[i2-1]/vols[i2-3],\
                    vols[i2-1]/vols[i2-2],vols[i2-2]/vols[i2-3],(vols[i2]+vols[i2-1])/(vols[i2-3]+vols[i2-2]),\
                    highs[i2]/highs[i2-1],highs[i2]/opens[i2-1],highs[i2]/lows[i2-1],highs[i2]/closes[i2-1],\
                    lows[i2]/highs[i2-1],lows[i2]/opens[i2-1],lows[i2]/lows[i2-1],lows[i2]/closes[i2-1],\
                    opens[i2]/highs[i2-1],opens[i2]/opens[i2-1],opens[i2]/lows[i2-1],opens[i2]/closes[i2-1],\
                    closes[i2]/closes[i2-1],closes[i2-4:i2].mean()/closes[i2-9:i2].mean(),highs[i2-4:i2].mean()/highs[i2-9:i2].mean(),\
                    closes[i2-4:i2].std()/closes[i2-9:i2].std(),highs[i2-4:i2].std()/highs[i2-9:i2].std(),\
                    np.std([ closes[i2],opens[i2],highs[i2],lows[i2] ])/np.std([closes[i2-1],opens[i2-1],highs[i2-1],lows[i2-1]])]
                Matrix.append(tem)
                if fig>0:
                    fig=fig-1
                    plt.figure()
                    candleData=[]
                    for i3 in range(i2-10,i2+3):
                        tem=(date2num(dates[i3]),opens[i3],highs[i3],lows[i3],closes[i3])
                        candleData.append(tem)
                    ax=plt.subplot()
                    ax.xaxis_date()
                    plt.xticks(rotation=45)
                    plt.yticks()
                    plt.title(stocks[i][0])
                    plt.xlabel('Date')
                    plt.ylabel('Price')
                    mpf.candlestick_ohlc(ax,candleData,width=0.8,colorup='r',colordown='g')
                    plt.grid()      
    
    conn.select_db(nameDB)
    Matrix=np.row_stack(Matrix)
    Matrix=np.column_stack((dateAll,Re,Matrix))
    cur.execute('drop table if exists indicators')
    cur.execute('create table if not exists indicators(date date,Re float,ind1 float,ind2 float,ind3 float,ind4 float,ind5 float,ind6 float,ind7 float,ind8 float,\
    ind9 float,ind10 float,ind11 float,ind12 float,ind13 float,ind14 float,ind15 float,ind16 float,ind17 float,ind18 float,ind19 float,ind20 float,ind21 float,ind22 float,\
    ind23 float,ind24 float,ind25 float,ind26 float,ind27 float,ind28 float)')
    cur.executemany('insert into indicators values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', Matrix.tolist()) 
    conn.commit()
    cur.close()
    conn.close()
    dateAll=Matrix[:,0]
    Re=Matrix[:,1]
    Matrix=Matrix[:,2:]
    hmmTestAll(Matrix,Re,0)    
    
selectInd=[0,6,7,9,10,13,14,15,16,17,18,21,23,24,]
#selectInd=range(0,25)
if sw1+sw2+sw3+sw4:  
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)     
    cur=conn.cursor()
    cur.execute('select * from indicators')
    Matrix=np.row_stack(cur.fetchall())
    dateAll=Matrix[:,0]
    Re=Matrix[:,1]
    Matrix=Matrix[:,2:]
    if sw4:
        Matrix=Matrix[:,selectInd]
    else:
        Matrix=Matrix[:,selectInd]
    
#    tem=sio.loadmat(saveData)
#    Matrix=tem['Matrix'] 
#    Rall=tem['Rall']
#    dateAll=tem['dateAll']
#    tem=[]
#    Re=Rall[:,1] #0:return1; 1:return2     

if sw1:    
#    pca=PCA(n_components=12)
#    Matrix=pca.fit_transform(Matrix[:,[0,4,7,8,9,12,13,14,15,16,18,21,26,27,28,29]])
    hmmTestAll(Matrix,Re,0)    
if sw2:    
    flagSelected=[ [0,[1,3]],[3,[1,2]],[4,[2]],[6,[0,2]],[7,[1,2]],[8,[2]],[9,[2]],[10,[3,4]],]
    flag=hmmTestCertain(Matrix,Re,flagSelected)  # flag is 1 or 0;
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('drop table if exists indSelected')
    cur.execute('create table if not exists indSelected(flag tinyint)')
    cur.executemany('insert into indSelected values(%s)', flag.tolist()) 
    conn.commit()
    cur.close()
    conn.close()
if sw3:
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('select * from indSelected')
    indSelected=np.column_stack(cur.fetchall())[0]>0
    Matrix=Matrix[indSelected,:] 
    Re=Re[indSelected]
    dateAll=dateAll[indSelected]
#    pca=PCA(n_components=4)
#    Matrix=pca.fit_transform(Matrix)
    flag=hmmTestAll(Matrix,Re,Matrix.shape[1])
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('drop table if exists flag')
    cur.execute('create table if not exists flag(flag tinyint)')
    cur.executemany('insert into flag values(%s)', flag.tolist()) 
    conn.commit()
    cur.close()
    conn.close()
    
    flagU=np.unique(flag)
    for i in range(len(flagU)):
        tem=flag==flagU[i]
        datei=dateAll[tem]
        Rei=Re[tem]
        Lt=len(datei)
        month=[]
        day=[]
        week=[]
        weekday=[]    
        for i2 in range(Lt):
            month.append(datei[i2].strftime('%m'))
            day.append(datei[i2].strftime('%d'))
            week.append(datei[i2].strftime('%W'))
            weekday.append(datei[i2].strftime('%w'))
        sortStatastic(weekday,Rei,'flag:'+str(flagU[i])+'--weekday')
        sortStatastic(month,Rei,'flag:'+str(flagU[i])+'--month')
        sortStatastic(day,Rei,'flag:'+str(flagU[i])+'--day')
        sortStatastic(week,Rei,'flag:'+str(flagU[i])+'--week')

if sw3_1:
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('select * from indicators')
    Matrix=np.row_stack(cur.fetchall())
    dateAll=Matrix[:,0]
    Re=Matrix[:,1]
    Matrix=Matrix[:,2:] 
    
#    Matrix=Matrix[:,selectInd] # select according to sw2; if comments, select according to raw data;
#    cur.execute('select * from indSelected')
#    indSelected=np.column_stack(cur.fetchall())[0]>0
#    Matrix=Matrix[indSelected,:] 
#    Re=Re[indSelected]
#    dateAll=dateAll[indSelected]

    Lt=len(dateAll)
    month=[]
    day=[]
    week=[]
    weekday=[]    
    for i in range(Lt):
        month.append(dateAll[i].strftime('%m'))
        day.append(dateAll[i].strftime('%d'))
        week.append(dateAll[i].strftime('%W'))
        weekday.append(dateAll[i].strftime('%w'))
    sortStatastic(weekday,Re,'weekday')
    sortStatastic(month,Re,'month')
    sortStatastic(day,Re,'day')
    sortStatastic(week,Re,'week')
    cur.close()
    conn.close()
    
if sw4:
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('select * from indSelected')
    indSelected=np.column_stack(cur.fetchall())[0]>0
    Matrix=Matrix[indSelected,:] 
    Re=Re[indSelected]
    dateAll=dateAll[indSelected]

    seqTrain(Matrix,Re,'seqTrain')
    for i in range(Matrix.shape[1]):
        seqTrain(Matrix[:,i],Re,'seqTrain'+'---column'+str(i))

#    cur.execute('select * from flag')
#    flag=np.column_stack(cur.fetchall())[0]
#    flagU=np.unique(flag)
##    flagU=[2] #2,4,1    
#    for i in range(len(flagU)):
#        indTem=flag==flagU[i]
#    
##        for i2 in range(Matrix.shape[1]):
##            X=Matrix[indTem,i2]
##            y=Re[indTem]
##            seqTrain(X,y,'flag:'+str(flagU[i])+'---indicator:'+str(i2))
#        X=Matrix[indTem]
#        y=Re[indTem]
#        seqTrain(X,y,'flag:'+str(flagU[i])+'---indicator:All')    

    cur.close()
    conn.close()
if sw5:
    tem=sio.loadmat(fileName+'Selected')
    flag_sw3=tem['flag_sw3'][0]
    Matrix=tem['Matrix']
    Re=tem['Re'][0]
    dateAll=tem['dateAll']
    PCAtest(Matrix,Re)

x2=time.clock()
print(x2-x1)

    



    



