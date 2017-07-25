Xshape=Xraw.shape
Xrow=Xshape[0]
Xcol=Xshape[1]
#    Xraw,X0,Re,y0=train_test_split(Xraw,np.array(Re),test_size=0.0)
for lp in range(Xcol):
    print(lp)
    X=Xraw[:,lp]
    trainSample=50000
    if Xrow<trainSample:
        Xtrain=X[:Xrow//2]
        Xtest=X[Xrow//2:]
        Retrain=Re[:Xrow//2]
        Retest=Re[Xrow//2:]
    else:
        Xtrain=X[:trainSample]
        Xtest=X[trainSample:]    
        Retrain=Re[:trainSample]  
        Retest=Re[trainSample:]
        
    hmm=GaussianHMM(n_components=5,covariance_type='diag',n_iter=10000).fit(np.row_stack(Xtrain)) #spherical,diag,full,tied 
    joblib.dump(hmm,fileSave+str(lp))
    
    for i in range(2):
        if i==0:
            Xtem=Xtrain
            Re=Retrain
        else:
            Xtem=Xtest
            Re=Retest
            
        flag=hmm.predict(np.row_stack(Xtem))
        plt.figure(figsize=(15,8))
        xi=[]
        yi=[]
        for i2 in range(hmm.n_components):
            state=(flag==i2)
            ReT=Re[state]
            ReTcs=ReT.cumsum()
            LT=len(ReT)
            if LT<2:
                continue
            maxDraw=0
            maxDrawi=0
            maxDrawValue=0
            i2High=0
            for i3 in range(LT):
                if ReTcs[i3]>i2High:
                    i2High=ReTcs[i3]
                drawT=i2High-ReTcs[i3]
                if maxDraw<drawT:
                    maxDraw=drawT
                    maxDrawi=i3
                    maxDrawValue=ReTcs[i3]
            xi.append(maxDrawi)
            yi.append(maxDrawValue)  
            plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                     %(i2,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
        plt.plot(xi,yi,'r*')
#        plt.xlabel(Mark,fontsize=16)
#        plt.legend(loc='upper',bbox_to_anchor=(0.0,1.0),ncol=1,fancybox=True,shadow=True)
        plt.legend(loc='upper left')
        plt.grid(1)    
    