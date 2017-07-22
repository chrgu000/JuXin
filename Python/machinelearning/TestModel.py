# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:38:05 2017

@author: Caofa
"""
#from hmmlearn.hmm import GaussianHMM
#import numpy as np
#
#
#if __name__=="__main__":
#    fileX=sys.argv[1]
#    fin=open(fileX,'r')
#    lines=fin.readlines()
#    X=[]
#    for i in range(len(lines)):
#        line=np.array(map(float,lines[i].strip().split(',')))   
#        X.append(line.tolist())
#    X=np.row_stack(X)
#    fin.close()
#    hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=1000).fit(X)
#    flag=hmm.predict(X)    
#    fout=open(fileX,'w')
#    for i in range(len(flag)):
#        fout.write('%d,' %flag[i])
#    fout.close()

from hmmlearn.hmm import GaussianHMM
import scipy.io as sio
import numpy as np


if __name__=="__main__":
    tem=sio.loadmat('e:\\Trading\\Matlab_Python.mat')
    X=tem['Matrix']
    
    X=[]
    for i in range(len(lines)):
        line=np.array(map(float,lines[i].strip().split(',')))   
        X.append(line.tolist())
    X=np.row_stack(X)
    fin.close()
    hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=1000).fit(X)
    flag=hmm.predict(X)    
    fout=open(fileX,'w')
    for i in range(len(flag)):
        fout.write('%d,' %flag[i])
    fout.close()
    
    
    
    