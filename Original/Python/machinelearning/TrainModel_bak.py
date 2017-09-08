# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 11:12:35 2017

@author: Administrator
"""

from hmmlearn.hmm import GaussianHMM
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
import joblib, warnings

warnings.filterwarnings("ignore")

class TrainModel():
    def __init__(self,nameDB):
        self.nameDB=nameDB
        self.saveData='D:\\Trade\\Original\\joblib\\'+nameDB
    def __call__(self,func):
        def _call(*args,**kw):
            print ('class decorator runing!')
            x=32;y=45
            return func(x,y)
        x= _call
        return x
    
    def hmmTestAll(self,Xraw,Reraw,figStart): # figStart: how many figs to show 0 means show all and Xcol mean show one (in all)
        Xshape=Xraw.shape
        Xrow=Xshape[0]
        Xcol=Xshape[1]
        if figStart!=Xcol:
            Xraw,X0,Reraw,y0=train_test_split(Xraw,np.array(Reraw),test_size=0.0) #random_state=1
        dispersity=[] # hold dispesity of each column but last one not for some one column but all;
        profitP=[] # hold each type's profit/per of each indicator column
        if figStart!=0:
            colStart=Xcol        
        else:
            colStart=0
        for lp in range(colStart,Xcol+1):
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
            if figStart!=0:
                Xtest=X
                Retest=Reraw
                figTitle=str(figStart)
    
            hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=10000).fit(np.row_stack(Xtrain)) #spherical,diag,full,tied 
            joblib.dump(hmm,self.saveData+figTitle+'_hmm')
            
    #        for i in range(2):
            records=[] # hold two recordi
            for i in range(2):
                
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
                recordi=[] # record number of total orders, IR,winratio,ratioWL,profitP
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
                    recordi.append([LT,np.mean(ReT)/np.std(ReT),ReTcs[-1]/LT*100])
                    plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                             %(i2,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
                records.append(recordi)
                plt.plot(xi,yi,'r*')
                plt.title(figTitle,fontsize=16)
                
                if i==1:
                    rec1=np.row_stack(records[0])
                    rec2=np.row_stack(records[1])
                    profitP.append(rec2[:,2].tolist())
                    orders=rec2[:,0]
                    tem=orders>rec2.max()/4
                    if tem.sum()>1:
                        orders=orders[tem]
                        tem=rec2[:,2][tem].std()*np.sqrt(tem.sum())/(np.std(orders/orders.max())+1)
                    else:
                        tem=0
                    dispersity.append(tem)
                    if tem>0.2:
                        plt.xlabel( 'indicator column %d, correlative of train and test: %.10f, dispesity:%.10f'\
                               %(lp,pd.DataFrame(rec1[:,1])[0].corr(pd.DataFrame(rec2[:,1])[0]), tem ),color='r')
                    else:
                        plt.xlabel( 'indicator column %d, correlative of train and test: %.10f, dispesity:%.10f'\
                               %(lp,pd.DataFrame(rec1[:,1])[0].corr(pd.DataFrame(rec2[:,1])[0]), tem ),color='gray')                        
        #        plt.legend(loc='upper',bbox_to_anchor=(0.0,1.0),ncol=1,fancybox=True,shadow=True)
                plt.legend(loc='upper left')
                plt.grid(1)
                
        if figStart==Xcol:
            return flag,profitP
        else:
            dispersity=np.array(dispersity)
            return dispersity,profitP
       
    def hmmTestCertainNot(self,Matrix,flagSelect):
        X=np.row_stack(Matrix)  
        Nind=[]
        flagNot=[]
        for i in range(len(flagSelect)):
            Nind.append(flagSelect[i][0])
            flagNot.append(flagSelect[i][1])            
        ReSelect=np.ones(len(X))
        for i2 in range(len(Nind)):    
            hmm=joblib.load(self.saveData+str(Nind[i2])+'_hmm')
            flagTem=hmm.predict(np.row_stack(X[:,Nind[i2]]))
            for i in range(len(flagNot[i2])):
                    ReSelect=ReSelect*(flagTem!=flagNot[i2][i])       
        return ReSelect
    
    def hmmTestCertainOk(self,Matrix,flagSelect):
        X=np.row_stack(Matrix)  
        Nind=[]
        flagOk=[]
        for i in range(len(flagSelect)):
            Nind.append(flagSelect[i][0])
            flagOk.append(flagSelect[i][1])            
        ReSelect=np.zeros(len(X))
        for i2 in range(len(Nind)):    
            hmm=joblib.load(self.saveData+str(Nind[i2])+'_hmm')
            flagTem=hmm.predict(np.row_stack(X[:,Nind[i2]]))
            for i in range(len(flagOk[i2])):
                    ReSelect=ReSelect+(flagTem==flagOk[i2][i])    
        return ReSelect
    
    def xgbTrain(self,x_train,y_train,x_test,y_test):
        x_train=x_train.copy()
        x_test=x_test.copy()
        y_train=y_train.copy()
        y_test=y_test.copy()        
        y_train[y_train>=0.003]=1
        y_train[y_train<=0.003]=0
        y_test[y_test>=0.003]=1
        y_test[y_test<0.003]=0
        
        data_train=xgb.DMatrix(data=x_train,label=y_train)
        data_test=xgb.DMatrix(data=x_test,label=y_test)
        watch_list={(data_test,'eval'),(data_train,'train')}
        param={'max_depth':3,'eta':0.03,'early_stopping_rounds':3,'silent':1,'objective':'multi:softmax','num_class':2}
        XGB=xgb.train(param,data_train,num_boost_round=1000,evals=watch_list) #modeify 20000
        joblib.dump(XGB,self.saveData+'_xgb')
    
    def xgbPredict(self,x_):
        data_=xgb.DMatrix(data=x_)
        XGB=joblib.load(self.saveData+'_xgb')
        return XGB.predict(data_)
        
    def gaussianNBtrain(self,x_,y_):
        y_train=y_.copy()
        y_train[y_train>=0.003]=1
        y_train[y_train<0.003]=0        
        gauNB=GaussianNB().fit(x_.tolist(),y_train.tolist())
        joblib.dump(gauNB,self.saveData+'_gauNB')
        
    def gaussianNBpredict(self,x_):
        gauNB=joblib.load(self.saveData+'_gauNB')
        return gauNB.predict(x_)
        
    
    def ReFig(self,Re,figTitle):
        for i in range(len(figTitle)):
            Rei=np.array(Re[i])
            figTitlei=figTitle[i]
            Recs=Rei.cumsum()
            LT=len(Rei)
            maxDraw=0
            maxDrawi=0
            maxDrawValue=0
            i2High=0
            for i2 in range(LT):
                if Recs[i2]>i2High:
                    i2High=Recs[i2]
                drawT=i2High-Recs[i2]
                if maxDraw<drawT:
                    maxDraw=drawT
                    maxDrawi=i2
                    maxDrawValue=Recs[i2]
            try:
                plt.plot(range(LT),Recs,label='%s ---- orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                     %(figTitlei,LT,np.mean(Rei)/np.std(Rei),sum(Rei>0)/float(LT),np.mean(Rei[Rei>0])/-np.mean(Rei[Rei<0]),maxDraw*100,Recs[-1]/LT*100))  
            except Exception as tem:
                plt.plot(range(LT),Recs)
                print(tem)
            plt.plot(maxDrawi,maxDrawValue,'r*')
            plt.legend(loc='upper left',framealpha=0.3)
            plt.grid(1) 
        plt.title(' VS '.join(figTitle))

    def sortStatastic(self,sorts,Re,Title):
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
    

    



    







    



