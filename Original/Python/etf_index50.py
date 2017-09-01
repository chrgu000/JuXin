# -*- coding: utf-8 -*-
"""
Created on Sat Jun 03 12:09:20 2017

@author: Cao Fa
"""

import tushare as ts
startDate='2010-01-01'
endDate='2017-06-02'
etf50=ts.get_hist_data('510050',start=startDate,end=endDate)
index50=ts.get_hist_data('000016',index=True,start=startDate,end=endDate)
