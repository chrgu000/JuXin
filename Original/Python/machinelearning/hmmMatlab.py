# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 13:29:58 2017
related to matlab procedure:HMM
@author: Administrator
"""
import numpy as np
import sys,joblib

# the number should be changed once HMMTest runs again;
if __name__=="__main__":
    infile=sys.argv[1]
    outfile=sys.argv[2]
    fin=open(infile,'r')
    fout=open(outfile,'w')
    lines=fin.readlines()
    hmm=joblib.load('D:\Trading\Python\machinelearning\HMMTest')
    X=[]
    for i in range(len(lines)):
        line=np.array(map(float,lines[i].strip().split(',')))   
        X.append(line.tolist())
    X=np.row_stack(X)
    flag=hmm.predict(X)
    flagMark=np.ones(len(flag))*-1
    indTem=flag==0
    flagMark[indTem]=1.34
    indTem=flag==1
    flagMark[indTem]=3.41
    indTem=flag==3
    flagMark[indTem]=1.44    
#    flag=flag<10
    for i in range(len(flag)):
        fout.write('%.2f,' %flagMark[i])
    fout.close()
    fin.close()
    
        
#    logReturn=(np.log(np.array(close[1:]))-np.log(np.array(close[:-1])))[4:]
#    logReturn5 = np.log(np.array(close[5:]))-np.log(np.array(close[:-5]))
#    diffReturn = (np.log(np.array(high))-np.log(np.array(low)))
