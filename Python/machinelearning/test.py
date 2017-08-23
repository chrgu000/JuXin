fig=10
conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
cur=conn.cursor()
cur.execute('create database if not exists '+nameDB) # create database;        
conn.select_db('pythonStocks')     
Lstocks=cur.execute('select number from stocks') # select name from stocks: get stocks' name;
Number=np.insert(np.cumsum(cur.fetchall()),0,0)
cur.execute('select name from stocks') # select name from stocks: get stocks' name;
stocks=cur.fetchall()
cur.execute('select * from dataDay') #'select * from dataDay limit '
dataAll=np.column_stack(cur.fetchall())

Re=[]
dateAll=[]
Matrix=[]
for i in range(Lstocks):
    print('%s:%d' %(stocks[i][0],i+1),end=' ',flush=True) #print(i, sep=' ', end=' ', flush=True)
    startT=Number[i]
    endT=Number[i+1]
    dates=dataAll[0][startT:endT]
    opens=dataAll[1][startT:endT]
    closes=dataAll[2][startT:endT]
    highs=dataAll[3][startT:endT]
    lows=dataAll[4][startT:endT]
    vols=dataAll[5][startT:endT]
    turns=dataAll[6][startT:endT]
    
    Lt=len(opens)
    if Lt<20:
        continue
#        maN=np.zeros(Lt)
#        ma10=np.zeros(Lt)
#        for i2 in range(10,Lt):
#            maN[i2]=np.mean(closes[i2-3:i2+1])
#            ma10[i2]=np.mean(closes[i2-10:i2+1])
    for i2 in range(15,Lt-3):
        if lows[i2-3]<=min(lows[i2-5:i2+1]) and highs[i2-2]>highs[i2-3] and highs[i2-1]>highs[i2] and lows[i2-1]>lows[i2] and \
        highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2] and closes[i2]/closes[i2-1]<1.095: #vols[i2-2:i2].min()>vols[[i2-3,i2]].max() and 
            if closes[i2+1]>closes[i2]:
                Re.append(closes[i2+2]/closes[i2]-1)
            else:
                Re.append(closes[i2+1]/closes[i2]-1)
            dateAll.append(dates[i2])
            max5near=max(closes[i2-4:i2+1]);max5far=max(closes[i2-9:i2-4]);
            min5near=min(closes[i2-4:i2+1]);min5far=min(closes[i2-9:i2-4]);
            max_7near=max(highs[i2-6:i2+1]);max_7far=max(highs[i2-13:i2-6]);
            min_7near=min(lows[i2-6:i2+1]);min_7far=min(lows[i2-13:i2-6]);
            if max5near>max5far and min5near>min5far:
                ud5=1
            elif max5near<max5far and min5near<min5far:
                ud5=-1
            else:
                ud5=0
            if max_7near>max_7far and min_7near>min_7far:
                ud_7=1
            elif max_7near<max_7far and min_7near<min_7far:
                ud_7=-1
            else:
                ud_7=0
                                   
            tem=[ max5near/max5far,min5near/min5far,vols[i2]/vols[i2-2],ud_7,\
                 pd.DataFrame([lows[i2-3],opens[i2-3],closes[i2-3],highs[i2-3]])[0].corr(pd.DataFrame([lows[i2],closes[i2],opens[i2],highs[i2]])[0]),\
                vols[i2]/vols[i2-3],vols[i2]/vols[i2-1],vols[i2-1]/vols[i2-3],\
                vols[i2-1]/vols[i2-2],vols[i2-2]/vols[i2-3],(vols[i2]+vols[i2-1])/(vols[i2-3]+vols[i2-2]),\
                highs[i2]/highs[i2-1],highs[i2]/opens[i2-1],highs[i2]/lows[i2-1],highs[i2]/closes[i2-1],\
                lows[i2]/highs[i2-1],lows[i2]/opens[i2-1],lows[i2]/lows[i2-1],lows[i2]/closes[i2-1],\
                opens[i2]/highs[i2-1],opens[i2]/opens[i2-1],opens[i2]/lows[i2-1],opens[i2]/closes[i2-1],\
                closes[i2]/closes[i2-1],closes[i2-4:i2].mean()/closes[i2-9:i2].mean(),highs[i2-4:i2].mean()/highs[i2-9:i2].mean(),\
                closes[i2-4:i2].std()/closes[i2-9:i2].std(),highs[i2-4:i2].std()/highs[i2-9:i2].std(),\
                np.std([ closes[i2],opens[i2],highs[i2],lows[i2] ])/np.std([closes[i2-1],opens[i2-1],highs[i2-1],lows[i2-1]])]
            Matrix.append(tem)
            if fig>0:
                fig=fig-1
                plt.figure()
                candleData=[]
                for i3 in range(i2-10,i2+3):
                    tem=(date2num(dates[i3]),opens[i3],highs[i3],lows[i3],closes[i3])
                    candleData.append(tem)
                ax=plt.subplot()
                ax.xaxis_date()
                plt.xticks(rotation=45)
                plt.yticks()
                plt.title(stocks[i][0])
                plt.xlabel('Date')
                plt.ylabel('Price')
                mpf.candlestick_ohlc(ax,candleData,width=0.8,colorup='r',colordown='g')
                plt.grid()      

conn.select_db(nameDB)
Matrix=np.row_stack(Matrix)
Matrix=np.column_stack((dateAll,Re,Matrix))
cur.execute('drop table if exists indicators')
cur.execute('create table if not exists indicators(date date,Re float,ind1 float,ind2 float,ind3 float,ind4 float,ind5 float,ind6 float,ind7 float,ind8 float,\
ind9 float,ind10 float,ind11 float,ind12 float,ind13 float,ind14 float,ind15 float,ind16 float,ind17 float,ind18 float,ind19 float,ind20 float,ind21 float,ind22 float,\
ind23 float,ind24 float,ind25 float,ind26 float,ind27 float,ind28 float,ind29 float)')
cur.executemany('insert into indicators values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', Matrix.tolist()) 
conn.commit()
cur.close()
conn.close()
dateAll=Matrix[:,0]
Re=Matrix[:,1]
Matrix=Matrix[:,2:]
dispersity,profitP=hmmTestAll(Matrix,Re,0)  
print('*'*100)
tem=np.array(dispersity[:-1]) # delete the last one which is not for single indicator but for all indicators;
indSelected=np.array(range(len(tem)))[tem>0.3]
hmmTestAll(Matrix[:,indSelected],Re,0) 
print(profitP)