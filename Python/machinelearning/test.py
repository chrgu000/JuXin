X = np.row_stack(Matrix)
X_train,X_test,y_train,y_test=train_test_split(X,Re,test_size=0.3)
y_trainLabel=np.ones(len(y_train))*3
indTem=y_train<-0.01
y_trainLabel[indTem]=1
indTem=(y_train>=-0.01)*(y_train<=0.01)
y_trainLabel[indTem]=2
y_testLabel=np.ones(len(y_test))*3
indTem=y_test<-0.01
y_testLabel[indTem]=1
indTem=(y_test>=-0.01)*(y_test<=0.01)
y_testLabel[indTem]=2

seq=StructuredPerceptron()
seq.fit(X_train,y_trainLabel,[len(y_train),])
#joblib.dump(hmm,'HMMTest')
y_pred=seq.predict(X_test,[len(y_test)])