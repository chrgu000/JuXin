# -*- coding: utf-8 -*-

import tushare as ts
import numpy as np

data=ts.get_hs300s()
stocks=data['code']
#stocks=np.load('stocks.npy')
numStocks=len(stocks)
dataTem=ts.get_stock_basics()
dataTem.to_csv('e:/TuData/stocksBasics.csv')

for i in range(0,numStocks-290):
    dataTem=ts.get_k_data(stocks[i],start='2013-01-01')
    dataTem.to_excel('e:/TuData/hs300/'+stocks[i]+'.xlsx')
    
print 'OK, data downloading is completed!'


'''
import mlab 
from mlab.releases import latest_release as matlab 
from numpy import * 
[u,s,v] = matlab.svd(array([[1,2], [1,3]]), nout=3)
matlab.path(matlab.path(),r'D:\Trading')
a=matlab.test

'''