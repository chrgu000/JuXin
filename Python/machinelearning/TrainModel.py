# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 16:27:07 2017

@author: Administrator
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:10:55 2017

@author: Administrator
"""


from hmmlearn.hmm import GaussianHMM
from seqlearn.perceptron import StructuredPerceptron
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io as sio
import joblib, warnings,pymysql,time
warnings.filterwarnings("ignore")
nameDB='TrainModel'
MatlabData='E:\Matlab2Python\R_Matrix'

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
#    Xraw,X0,Re,y0=train_test_split(Xraw,np.array(Re),test_size=0.0)
    for lp in range(figStart,Xcol+1):
        if lp<Xcol:
            X=Xraw[:,lp]
            figTitle=str(lp)
        else:
            X=Xraw
            figTitle='All'
        trainSample=50000
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
            
        hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=10000).fit(np.row_stack(Xtrain)) #spherical,diag,full,tied 
        joblib.dump(hmm,fileSave+figTitle)
        
#        for i in range(2):
        for i in range(1):
            i=1
            
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
            hmm=joblib.load(fileSave+str(Nind[i2]))
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
    indTem=y_train<0.0
    y_trainLabel[indTem]=1
    y_testLabel=np.ones(len(y_test))*3
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
    
    seq=StructuredPerceptron()
    seq.fit(X_train,y_trainLabel,[len(y_train),])
    #joblib.dump(hmm,'HMMTest')
    y_pred=seq.predict(X_test,[len(y_test)])
#    svm=SVC(kernel='rbf',random_state=0,gamma=0.010,C=1)
#    svm.fit(X_train,y_trainLabel)
#    y_pred=svm.predict(X_test)
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
    
    
    


sw0=1 # get dataset for the model;
sw1=0 # test all for the first time
sw2=0 # show figure after delete some bad type (should be done by hand)
sw3=0 # test all for the second time after delete some bad type
sw4=0 # train by seq   
sw5=0 # PCA

if sw0:   
#    x1=time.clock()
#    
#    conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
#    cur=conn.cursor()
#    cur.execute('create database if not exists '+nameDB) # create database;        
#    conn.select_db('pythonStocks')            
#    stocks = pd.read_sql('show tables',con=conn)
#    Re=[]
#    dateAll=[]
#    Matrix=[]
#    for i in range(stocks.shape[0]-1):
#        print('stocks:%d' %(i+1))
#        tem=pd.read_sql('select * from '+stocks.loc[0][0],con=conn)
#        dates=tem['date']
#        opens=tem['open']
#        closes=tem['close']
#        highs=tem['high']
#        lows=tem['low']
#        vols=tem['vol']
#        turns=tem['turn']
#        Lt=opens.shape[0]
#        if Lt<20:
#            continue
#        maN=np.zeros(Lt)
#        ma10=np.zeros(Lt)
#        for i2 in range(10,Lt):
#            maN[i2]=np.mean(closes.loc[i2-3:i2])
#            ma10[i2]=np.mean(closes.loc[i2-10:i2])
#        for i2 in range(12,Lt-3):
#            if lows[i2-3]<=min(lows.loc[i2-5:i2]) and highs[i2-2]>highs[i2-3] and highs[i2-1]>highs[i2] and lows[i2-1]>lows[i2] and \
#            min(vols.loc[i2-2:i2-1])>max(vols[[i2,i2-3]]) and highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2]:
#                if closes[i2+1]>closes[i2]:
#                    Re.append(closes[i2+2]/closes[i2])
#                else:
#                    Re.append(closes[i2+1]/closes[i2])
#                dateAll.append(dates[i2])
#                tem=[ pd.DataFrame([lows[i2-3],opens[i2-3],closes[i2-3],highs[i2-3]])[0].corr(pd.DataFrame([lows[i2],closes[i2],opens[i2],highs[i2]])[0]),\
#                    pd.DataFrame([lows[i2-2],opens[i2-2],closes[i2-2],highs[i2-2]])[0].corr(pd.DataFrame([lows[i2-1],closes[i2-1],opens[i2-1],highs[i2-1]])[0]),\
#                    pd.DataFrame([lows[i2-3],opens[i2-3],closes[i2-3],highs[i2-3],lows[i2-2],opens[i2-2],closes[i2-2],highs[i2-2]])[0].corr(pd.DataFrame(\
#                                [lows[i2],closes[i2],opens[i2],highs[i2],lows[i2-1],closes[i2-1],opens[i2-1],highs[i2-1]])[0]),\
#                    vols[i2]/vols[i2-3],vols[i2]/vols[i2-2],vols[i2]/vols[i2-1],vols[i2-1]/vols[i2-3],\
#                    vols[i2-1]/vols[i2-2],vols[i2-2]/vols[i2-3],(vols[i2]+vols[i2-1])/(vols[i2-3]+vols[i2-2]),\
#                    highs[i2]/highs[i2-1],highs[i2]/opens[i2-1],highs[i2]/lows[i2-1],highs[i2]/closes[i2-1],\
#                    lows[i2]/highs[i2-1],lows[i2]/opens[i2-1],lows[i2]/lows[i2-1],lows[i2]/closes[i2-1],\
#                    opens[i2]/highs[i2-1],opens[i2]/opens[i2-1],opens[i2]/lows[i2-1],opens[i2]/closes[i2-1],\
#                    closes[i2]/highs[i2-1],closes[i2]/opens[i2-1],closes[i2]/lows[i2-1],closes[i2]/closes[i2-1],\
#                    np.mean(closes[i2-4:i2])/np.mean(closes[i2-9:i2]),np.mean(highs[i2-4:i2])/np.mean(highs[i2-9:i2]),\
#                    np.std(closes[i2-4:i2])/np.std(closes[i2-9:i2]),np.std(highs[i2-4:i2])/np.std(highs[i2-9:i2]),\
#                    np.std([ closes[i2],opens[i2],highs[i2],lows[i2] ])/np.std([closes[i2-1],opens[i2-1],highs[i2-1],lows[i2-1]])]
#                Matrix.append(tem)
#    x2=time.clock()
#    print(x2-x1)
    

if sw1+sw2+sw3:        
    tem=sio.loadmat(MatlabData)
    Matrix=tem['Matrix'] 
    Rall=tem['Rall']
    dateAll=tem['dateAll']
    tem=[]
    Re=Rall[:,1] #0:return1; 1:return2     
if sw1:    
    hmmTestAll(Matrix,Re,0)    
if sw2:    
    flagSelected=[ [2,[2]],[3,[1,4]],[4,[3]],[6,[4]],[7,[1]],[8,[1,2]],[9,[2,4]],[10,[1,4]],[11,[1,4]],\
                  [12,[2]],[13,[2]],[14,[0,3]],[15,[4]],[17,[4]],[18,[4]],[19,[3]],[20,[3,4]],[25,[4]],[25,[4]] ]
    flag=hmmTestCertain(Matrix,Re,flagSelected) 
    sio.savemat(fileName+'Selected',{'flag':flag})
if sw3:
    tem=sio.loadmat(fileName+'Selected')
    flag_sw2=tem['flag_sw2'][0]>0
    Matrix=Matrix[flag_sw2,:] 
    Re=Re[flag_sw2]
    dateAll=dateAll[flag_sw2]
#    hmmTestAll(Matrix[:,[0,1,3,9,10,11,14,15,17,23,24,25]],Re)
    flag_sw3=hmmTestAll(Matrix,Re,Matrix.shape[1])
    sio.savemat(fileName+'Selected',{'flag_sw2':flag_sw2,'flag_sw3':flag_sw3,'Matrix':Matrix,'Re':Re,'dateAll':dateAll})
if sw4:
    tem=sio.loadmat(fileName+'Selected')
    flag_sw3=tem['flag_sw3'][0]
    Matrix=tem['Matrix']
    Re=tem['Re'][0]
    dateAll=tem['dateAll']

#    flagU=np.unique(flag_sw3)
    flagU=[2] #2,4,1
    
    for i in range(len(flagU)):
        indTem=flag_sw3==flagU[i]
        
        for i2 in range(Matrix.shape[1]):
            X=Matrix[indTem,i2]
            y=Re[indTem]
            seqTrain(X,y,'flag:'+str(flagU[i])+'---indicator:'+str(i2))
#        X=Matrix[indTem,:]
#        X=X[:,[4,5,29,30]]
#        y=Re[indTem]        
#        seqTrain(X,y,'flag:'+str(flagU[i])+'---indicator:assembly')
if sw5:
    tem=sio.loadmat(fileName+'Selected')
    flag_sw3=tem['flag_sw3'][0]
    Matrix=tem['Matrix']
    Re=tem['Re'][0]
    dateAll=tem['dateAll']
    PCAtest(Matrix,Re)

    



    



