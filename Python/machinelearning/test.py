

MatrixXGB=Matrix
x_train,x_test,y_train,y_test=train_test_split(MatrixXGB,ReXGB,random_state=0,test_size=0.4)
recordPoint=[]
tem=np.linspace(0.03,-0.03,600,endpoint=0)
for i in tem:
    recordPoint.append((y_train>i).sum())
recordPoint=np.array(recordPoint)
point1=tem[(recordPoint<=len(y_train)/3).sum()-1]
point2=tem[(recordPoint<=len(y_train)*2/3).sum()-1]
y_train_raw=y_train.copy()
y_train[y_train_raw>=point1]=2
y_train[(y_train_raw>point2) * (y_train_raw<point1)]=1
y_train[y_train_raw<=point2]=0
y_test_raw=y_test.copy()
y_test[y_test_raw>=point1]=2
y_test[(y_test_raw>point2) * (y_test_raw<point1)]=1
y_test[y_test_raw<=point2]=0
data_train=xgb.DMatrix(x_train,label=y_train)
data_test=xgb.DMatrix(x_test,label=y_test)
watch_list={(data_test,'eval'),(data_train,'train')}
param={'max_depth':2,'eta':0.1,'silent':1,'objective':'multi:softmax','num_class':3}
bst=xgb.train(param,data_train,num_boost_round=2000,evals=watch_list)

y_pre=bst.predict(data_train)
flags=np.unique(y_pre)
Rex=[];labelx=[]
for i in range(len(flags)):
    tem=y_pre==flags[i]
    Rex.append(y_train_raw[tem].tolist())
    labelx.append('train'+str(flags[i]))
TM.ReFig(Rex,labelx)
y_pre=bst.predict(data_test)
flags=np.unique(y_pre)
Rex=[];labelx=[]
for i in range(len(flags)):
    tem=y_pre==flags[i]
    Rex.append(y_test_raw[tem].tolist())
    labelx.append('test'+str(flags[i]))
TM.ReFig(Rex,labelx)
































