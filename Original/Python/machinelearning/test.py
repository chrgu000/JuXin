x_=Matrix
y=Re

#pca=PCA(n_components=0.98)
#newMatrix=pca.fit_transform(x) 

#for i2 in range(29):
kmean=KMeans(n_clusters=5)
kmean.fit((Matrix[:,[0,1,14,26]]))
labels=kmean.labels_
labelsU=np.unique(labels)
Rlist=[];titles=[];
for i in range(len(labelsU)):
    tem=labels==labelsU[i]
    Rlist.append(y[tem])
    titles.append(str(i2)+'flagsNew:'+str(i))
plt.figure(figsize=(15,8))
TM.ReFig(Rlist,titles)