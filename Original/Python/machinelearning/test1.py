# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 13:25:50 2017

@author: Administrator
"""

Lt=Matrix.shape[1]
P=[]
for i in range(Lt):
    x=Matrix[:,i]
    xS=x.copy()
    xS.sort()
    tem=len(x)/5
    p1=xS[int(tem)]
    p2=xS[int(tem*2)]
    p3=xS[int(tem*3)]
    p4=xS[int(tem*4)]
    P.append([p1,p2,p3,p4])
    r1=Re[x<p1]
    r2=Re[(x<p2)*(x>=p1)]
    r3=Re[(x<p3)*(x>=p2)]
    r4=Re[(x<p4)*(x>=p3)]
    r5=Re[(x>=p4)]
    plt.figure()
    re=[]
    title=[]
    if len(r1)>0:
        re.append(r1)
        title.append(str(i)+'--r1')
    if len(r2)>0:
        re.append(r2)
        title.append(str(i)+'--r2')
    if len(r3)>0:
        re.append(r3)
        title.append(str(i)+'--r3')
    if len(r4)>0:
        re.append(r4)
        title.append(str(i)+'--r4')
    if len(r5)>0:
        re.append(r5)
        title.append(str(i)+'--r5')
    TM.ReFig(re,title)
    

    