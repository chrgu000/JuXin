# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:40:56 2017

@author: Administrator
"""
from WindPy import *
w.start()

#登陆账号
w.tlogon('0000', '0', 'W115294100301', '*********', 'SHSZ')

#平仓
data= w.tquery('Position')
stocksHold=data.Data[0]
sharesAvailable=data.Data[3]
Ltem=len(stocksHold)
for i in range(Ltem):
    w.torder(stocksHold[i], 'Sell', '0', sharesAvailable[i], 'OrderType=B5TC')
