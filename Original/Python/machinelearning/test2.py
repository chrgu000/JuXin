import matplotlib.pyplot as plt
import numpy as np
def gini(p):
    return 1-p**2-(1-p)**2
def entropy(p):
    return -p*np.log2(p)-(1-p)*np.log2(1-p)
x=np.arange(0.0,1.0,0.01)
ent=[entropy(p) if p!=0 else None for p in x]
sc_ent=[e*0.5 if e else None for e in ent]
fig=plt.figure(figsize=(8,6))
data=[ent,sc_ent,gini(x)]
lab=['Entropy','Entropy(*0.5)','Gini Impurity']
styles=['-','--','-.']
for i in range(3):
    line=plt.plot(x,data[i],linestyle=styles[i],lw=2,label=lab[i])
    
plt.legend(loc='upper center',bbox_to_anchor=(0.5,1.15),ncol=3)
plt.axhline(y=0.5,linewidth=1,color='k',linestyle='--')
plt.axhline(y=1.0,linewidth=1,color='k',linestyle='--')
plt.ylim([0,1.1])
plt.xlabel('p')
plt.ylabel('Impurity Index')
plt.show()






















