# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:02:11 2017

@author: Administrator
"""

from WindPy import *
import numpy as np
import datetime


PeriodFrom=1
PeriodTo=5
w.start()
today=datetime.date.today()
dataTem=w.wsi('10000904.sh','open,close','2017-5-25',today,'periodstart=09:31:00;periodend=15:01:00','BarSize='+str(PeriodFrom)+';Fill=Previous')
open1=np.array(dataTem.Data[0])
close1=np.array(dataTem.Data[1])
dataTem=w.wsi('10000905.sh','open,close','2017-5-25',today,'periodstart=09:31:00;periodend=15:01:00','BarSize='+str(PeriodFrom)+';Fill=Previous')
open2=np.array(dataTem.Data[0])
close2=np.array(dataTem.Data[1])
High=[]
Low=[]
Open=[]
Close=[]
fromsPer=240/PeriodFrom
Ldays=len(open1)/fromsPer
for i in range(Ldays):
    openT=open1[i*fromsPer:(i+1)*fromsPer-1]-open2[i*fromsPer:(i+1)*fromsPer-1]
    closeT=close1[i*fromsPer:(i+1)*fromsPer-1]-close2[i*fromsPer:(i+1)*fromsPer-1]
    
    
    
    
    
    
    
    
    
    
    
    
    