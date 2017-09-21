dataTem=w.wsd('000001.sh','close,high,low,volume','2010-10-05','2017-9-21','PriceAdj=F')
close=dataTem.Data[0]
high=dataTem.Data[1][5:]
low=dataTem.Data[2][5:]
vol=dataTem.Data[3][5:]
money=dataTem.Data[3][5:]
dateList=pd.to_datetime(dataTem.Times[5:])
logReturn=(np.log(np.array(close[1:]))-np.log(np.array(close[:-1])))[4:]
logReturn5 = np.log(np.array(close[5:]))-np.log(np.array(close[:-5]))
diffReturn = (np.log(np.array(high))-np.log(np.array(low)))
closeidx = np.array(close[5:])
X = np.column_stack([logReturn,logReturn5,diffReturn])

latent_states_sequence=hmm.predict(X)
sns.set_style('white')
plt.figure(figsize=(15,8))
for i in range(hmm.n_components):
    state=(latent_states_sequence==i)
    plt.plot(dateList[state],closeidx[state],'.',label='latent state %d' %i,lw=1)
plt.legend()
plt.grid(1)

data=pd.DataFrame({'dateList':dateList,'logReturn':logReturn,'state':latent_states_sequence}).set_index('dateList')
plt.figure(figsize=(15,8))
for i in range(hmm.n_components):
    state=(latent_states_sequence==i)
    idx=np.append(0,state[:-1])
    tem=data.logReturn.multiply(idx,axis=0)
    plt.plot(np.exp(tem.cumsum()),label='latent_state %d;orders:%d'%(i,sum(state)) )
    #data['state %d_return'%i]=data.logReturn.multiply(idx,axis=0)
    #plt.plot(np.exp(data['state %d_return'%i].cumsum()),label='latent_state %d'%i)
plt.legend()
plt.grid(1)

