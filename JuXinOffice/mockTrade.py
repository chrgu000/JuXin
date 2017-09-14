# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:45:15 2017

@author: Administrator
"""

from WindPy import *

w.start()


def DemoWSQCallback(indata):
     print ("hello")
     for k in range(0,len(indata.Fields)):
         if(indata.Fields[k] == "rt_last"):
            lastvalue = str(indata.Data[k][0]);
            print (lastvalue)

 

live_data=w.wsq("000001.SH,000001.SZ","rt_last",func=DemoWSQCallback)


#http://www.dajiangzhang.com/q?c117c569-f6c7-4c1d-84a8-1c1c006a172d

#from WindPy import *
#w.start();
#
##open a file to write.
#pf = open('c:\\pywsqdataif.data', 'w')
#
##define the callback function
#def myCallback(indata):
#    if indata.ErrorCode!=0:
#        print('error code:'+str(indata.ErrorCode)+'\n');
#        return();
#
#    global begintime
#    lastvalue ="";
#    for k in range(0,len(indata.Fields)):
#         if(indata.Fields[k] == "RT_TIME"):
#            begintime = indata.Data[k][0];
#         if(indata.Fields[k] == "RT_LAST"):
#            lastvalue = str(indata.Data[k][0]);
#
#    string = str(begintime) + " " + lastvalue +"\n";
#    pf.writelines(string)
#    print(string);
#
#    #应该在w.cancelRequest后调用pf.close()
#    #pf.close();
#
# 
#
##to subscribe if14.CFE
#w.wsq("IF.CFE","rt_time,rt_last",func=myCallback)








