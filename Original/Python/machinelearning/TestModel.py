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
import sys,joblib

if __name__=="__main__":
    Nsort=int(sys.argv[1])
    Nfit=int(sys.argv[2])
    
#    fileName='e:\\Trade\\Matlab_Python.mat'
#    xtem=[1,2,3,1,2,1,3,4,6,5,6,5,4,3,2,1,4,5,6,3];
#    sio.savemat(fileName, {'flag':xtem })
    fileName='e:\\Trade\\Matlab_Python.mat'
    tem=sio.loadmat(fileName)
    X=tem['Matx']
    hmm=GaussianHMM(n_components=Nsort,covariance_type='diag',n_iter=Nfit).fit(X)
    joblib.dump(hmm,'TestModelHMM')
#    hmm=joblib.load('TestModelHMM')
    flag=hmm.predict(X)    
    sio.savemat(fileName, {'flag': flag})
    
    
    
    