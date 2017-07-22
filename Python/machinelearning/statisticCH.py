# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 11:27:01 2017

@author: Administrator
"""

from WindPy import *
from sklearn.cluster import KMeans
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt
import datetime

try:
    data = np.loadtxt('test.txt')  
except:
    w.start()
    dateNow=datetime.datetime.strftime(datetime.date.today(),'%Y%m%d')
    Tem=w.wsd('ic00.cfe','open,close','20150416',dateNow)
    Date=Tem.Times
    IC=Tem.Data
    Tem=w.wsd('ih00.cfe','open,close','20150416',dateNow)
    IH=Tem.Data
    Tem=w.wsi('ih00.cfe','close','20150416 09:00:00',dateNow+' 15:01:00','periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
    IHminutes=np.array(Tem.Data[0])
    Time=Tem.Times    
    Tem=w.wsi('ic00.cfe','close','20150416 09:00:00',dateNow+' 15:01:00','periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F');
    ICminutes=np.array(Tem.Data[0])
    IHOpen=np.array(IH[0])
    IHClose=np.array(IH[1])
    ICOpen=np.array(IC[0])
    ICClose=np.array(IC[1])
    L=len(IHOpen)
    wk1=[]
    wk2=[]
    wk3=[]
    wk4=[]
    wk5=[]
    for i in range(2,L):
        wd=Date[i].weekday()+1
        std=(ICminutes[(i-1)*241+1:(i-1)*241+241]/ICClose[i-2]-\
            IHminutes[(i-1)*241+1:(i-1)*241+241]/IHClose[i-2]).std()
        up_1=ICClose[i-1]/ICClose[i-2]-IHClose[i-1]/IHClose[i-2]
        up=ICClose[i]/ICClose[i-1]-IHClose[i]/IHClose[i-1]
        if wd==1:
            wk1.append([up_1,std,up])
        elif wd==2:
            wk2.append([up_1,std,up])
        elif wd==3:
            wk3.append([up_1,std,up])
        elif wd==4:
            wk4.append([up_1,std,up])
        elif wd==5:
            wk5.append([up_1,std,up])
        else:
            print 'weekday is %.1f' %wd
    for i in range(1,6):
        wk=np.array(eval('wk'+str(i)))
        title=u'weekday-'+str(i)
        x=wk[:,0:2]
        y=wk[:,2]        
#        littleD=0.002
#        ind1=np.where(y>littleD)
#        ind2=np.where(y<-littleD)
#        ind=np.hstack((ind1,ind2))
#        ind.sort()
#        x=x[ind,:][0]
#        y=y[ind][0]        
        y=[1 if y[ii]>0 else 0 for ii in range(len(y))]
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)
        sc=StandardScaler()
        sc.fit(x_train)
        x_train=sc.transform(x_train)
        x_test=sc.transform(x_test)
        
#        ppn = Perceptron(n_iter=100,eta0=0.1,random_state=0)
#        ppn.fit(x_train,y_train)
#        y_pred=ppn.predict(x_test)
        
        svm=SVC(kernel='linear',C=1.0,random_state=0) #'rbf'
        svm.fit(x_train,y_train)
        y_pred=svm.predict(x_test)        
        
        print 'Test: Accuracy- %.2f%%,All samples- %d' \
        % (100*accuracy_score(y_test,y_pred),len(y_test))
        y_pred=ppn.predict(x_train)
        print 'Train: Accuracy- %.2f%%,All samples- %d' \
        % (100*accuracy_score(y_train,y_pred),len(y_train))

#        km=KMeans(n_clusters=2,init='random',n_init=10,max_iter=300,tol=1e-04,\
#                  random_state=0)
#        y_km=km.fit_predict(x)
#        plt.figure(figsize=(18,12))
#        plt.scatter(x[y_km==0,0],x[y_km==0,1],s=50,c='lightgreen',marker='s',\
#                    label='cluster 1')
#        plt.scatter(x[y_km==1,0],x[y_km==1,1],s=50,c='orange',marker='o',\
#                    label='cluster 2')
#        #plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],s=250,\
#        #            marker='*',c='red',label='centroids')
#        plt.scatter(x[y>0.005,0],x[y>0.005,1],s=30,c='red',marker='+',\
#                    label='cluster up')
#        plt.scatter(x[y<=-0.002,0],x[y<=-0.002,1],s=30,c='blue',marker='+',\
#                    label='cluster down')   
#        plt.title(title)         
#        plt.legend()
#        #plt.grid()
#        plt.show()

            
        
        
        
        
        
        