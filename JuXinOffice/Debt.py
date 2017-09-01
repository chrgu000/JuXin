# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 13:47:23 2017

@author: Administrator
"""
from WindPy import *
import matplotlib.pyplot as plt
import numpy as np


w.start()

#data5=w.wsi('TF.CFE','close','2012-04-01 09:00:00','2017-09-01 09:00:00','periodstart=09:15:00;periodend=15:16:00;Fill=Previous;PriceAdj=F')
#data10=w.wsi('T.CFE','close','2012-04-01 09:00:00','2017-09-01 09:00:00','periodstart=09:15:00;periodend=15:16:00;Fill=Previous;PriceAdj=F')
data5=w.wsd('TF.CFE','close','2010-04-01','2017-09-01 ','Fill=Previous;PriceAdj=F')
data10=w.wsd('T.CFE','close','2010-04-01','2017-09-01 ','Fill=Previous;PriceAdj=F')
times=np.array([i.strftime('%Y-%m-%d') for i in data5.Times])

p5=np.array(data5.Data[0])
p10=np.array(data10.Data[0])
tem=np.min([len(p5)-np.isnan(p5).sum(),len(p10)-np.isnan(p10).sum()])
times=times[-tem:]
p5=p5[-tem:]
p10=p10[-tem:]

plt.plot(p5-p10)
tem=list(map(int,np.linspace(0,len(times),12,endpoint=0)))
plt.xticks(tem,times[tem],rotation=60)
plt.grid()

