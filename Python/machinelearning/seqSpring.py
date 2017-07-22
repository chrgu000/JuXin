# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:34:43 2017

@author: Administrator
"""

from seqlearn.perceptron import StructuredPerceptron
from sklearn.cross_validation import train_test_split

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys,joblib

#if __name__=="__main__":
#    infile=sys.argv[1]
#    dataTem=pd.read_csv(infile, sep=',', header=None, dtype=float, na_filter=False)    
dataTem=pd.read_csv('D:\Trading\hmmMatlabIn.txt', sep=',', header=None, dtype=float, na_filter=False)
Re1=dataTem[0]  # close(ii+1)/close(ii)-1.003
Re2=dataTem.iloc[:,1] #close(ii+2)/close(ii)-1.003
Date=dataTem.iloc[:,-1] # date of this day
factor1 = dataTem[2] # close(ii)/close(ii-1) IR: 0.3624,0.0575,0.0556,0.0229,0.0053
factor2 = dataTem[3] # std([close(ii);open(ii);low(ii);high(ii)])/std([close(ii-1);open(ii-1);low(ii-1);high(ii-1)])
factor3 = dataTem[4] # maN(ii)/ma10(ii)  IR: 0.138,0.077,0.0328,0.0284,0.0017
factor4 = dataTem[5] # close(ii)/close(ii-4) IR:1698(4591),0.0675,0.0631,-0.0055
factor5 = dataTem[6] # high(ii)/high(ii-1) IR:0.1908(orders:1045),0.0702,0.065,0.0008,-0.0135
factor6 = dataTem[7] # low(ii)/low(ii-1) IR: 0.1347,0.0356,0.0269,0.0097,0.0025
factor7 = dataTem[8] # close(ii)/close(ii-2) IR:0.237,0.0553,0.0528,0.0183,
factor8 = dataTem[9] # open(ii)/open(ii-1)
factor9 = dataTem[10] # close(ii)/high(ii-1)
factor10 = dataTem[11] # close(ii)/mean([low(ii-1),high(ii-1)]),
X = np.column_stack([factor2]) #factor2,factor3,factor5,factor6,factor9 #2 4 10
X_train,X_test,y_train,y_test=train_test_split(X,Re1,test_size=0.3)
y_trainLabel=np.ones(len(y_train))*3
indTem=y_train<-0.01
y_trainLabel[indTem]=1
indTem=(y_train>=-0.01)&(y_train<=0.01)
y_trainLabel[indTem]=2
y_testLabel=np.ones(len(y_test))*3
indTem=y_test<-0.01
y_testLabel[indTem]=1
indTem=(y_test>=-0.01)&(y_test<=0.01)
y_testLabel[indTem]=2

#hmm=joblib.load('D:\Trading\Python\machinelearning\HMMTest')
#latent_states_sequence=hmm.predict(X)  
#indTem=(latent_states_sequence==2)
#ReSelected=Re1[indTem]
#DateSelected=Date[indTem]
#fout=open('D:\Trading\hmmMatlabOut.txt','w')
#for i in range(len(ReSelected)):
#    fout.writelines('%.5f,%d\n' %(ReSelected.iloc[i],DateSelected.iloc[i]))
#fout.close()

seq=StructuredPerceptron()
seq.fit(X_train,y_trainLabel,[len(y_train),])
#joblib.dump(hmm,'HMMTest')
y_pred=seq.predict(X_test,[len(y_test)])
print 'accuracy:%.3f%%' %( (y_testLabel==y_pred).sum()*100/float(len(y_test)) )

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
        if ReTcs.iloc[i2]>i2High:
            i2High=ReTcs.iloc[i2]
        drawT=i2High-ReTcs.iloc[i2]
        if maxDraw<drawT:
            maxDraw=drawT
            maxDrawi=i2
            maxDrawValue=ReTcs.iloc[i2]
    xi.append(maxDrawi)
    yi.append(maxDrawValue)  
    plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.2f%%;'\
             %(i,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs.iloc[-1]/LT*100))  
plt.plot(xi,yi,'r*')
plt.legend()
plt.grid(1)



























