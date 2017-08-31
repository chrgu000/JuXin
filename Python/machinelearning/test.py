x=[]
for i in range(len(ReSelectOk)):
    tem=[Matrix[10:12].tolist(),Matrix[i].tolist()]
    tem1=TM.hmmTestCertainOk(tem,flagOk)[-1] >0
    tem2=ReSelectOk[i]>0
    x.append(tem1==tem2)
    
print(np.sum(x)/len(x))


