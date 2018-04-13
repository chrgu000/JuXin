tmp=len(Ptrain)//8
lgb_train = lgb.Dataset(Ftrain[tmp:,:], Ptrain[tmp:]>0)
lgb_eval = lgb.Dataset(Ftrain[:tmp,:], Ptrain[:tmp]>0, reference=lgb_train)
params = {
'max_depth':12,
'objective': 'binary',
'learning_rate': 0.02,
}
gbm = lgb.train(params,lgb_train,num_boost_round=20000,valid_sets=lgb_eval,early_stopping_rounds=15)
ProfitP=gbm.predict(Ftest, num_iteration=gbm.best_iteration)


tmp=ProfitP>0.5



Pselect=Ptest[tmp]
Dselect=Dtest[tmp]

def plotProfit(Pselect,legend):
    winRatio=sum(Pselect>0)/len(Pselect)
    IC=np.mean(Pselect)/np.std(Pselect)
    maxDown=0
    Pcumsum=Pselect.cumsum()
    for i in range(1,len(Pselect)):
        tmp=max(Pcumsum[:i])-Pcumsum[i]
        if tmp>maxDown:
            maxDown=tmp
    tmp=legend+':'+'winRatio {}%,IC:{},maxDown {}%,orders {}'.format(round(winRatio*100,2),round(IC,2),round(maxDown*100,2),len(Pselect))
    plt.plot(Pcumsum,label=tmp)
    plt.legend()

plt.figure(figsize=(10,6))
plotProfit(Pselect,'Predict Result')
plt.grid()

t3=time.time()
if reGetFeature:
    print('Preparing for Data consumes time {} minutes'.format(round((t01-t0)/60,2)))
    print('Extracting features and profits consumes time {} minutes'.format(round((t2-t01)/60,2)))
else:
    print('Extracting features and profits consumes time {} minutes'.format(round((t2-t0)/60,2)))
print('xgb training consumes all time {} minutes'.format(round((t3-t2)/60,2)))

plt.figure(figsize=(10,6))
wd=[i.weekday() for i in Dselect]
wdUni=np.unique(wd)
for i in wdUni:
    tmp=wd==i
    Proi=Pselect[tmp]
    plotProfit(Proi,'week day '+str(i+1))
plt.grid()
    