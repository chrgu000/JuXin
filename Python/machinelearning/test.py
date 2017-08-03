from WindPy import *
import numpy as np
import pymysql,datetime

sw1=0 # load stocks' data from wind and save it into MySQL;
sw2=1 # load new stocks' data (comparing to sw1) from wind and add them into MySQL;

today=datetime.date.today()
yesterday=today-timedelta(days=1)
w.start()
tem=w.wset('sectorconstituent','a001010100000000')
stocks=tem.Data[1]

Lt=len(stocks)
conn=pymysql.connect('localhost','caofa','caofa','pythonStocks')
cur=conn.cursor()
tem=cur.execute('select * from 000001SZ')
cur.scroll(tem-1,'absolute')
dateStart=cur.fetchone()[0]+datetime.timedelta(days=1)    
cur.execute('select * from stocks')
stocksRaw=set([i[0] for i in cur.fetchall()])
stocks=set(stocks)
stocksAdd=list(stocks-stocksRaw)
stocksRaw=list(stocksRaw & stocks) # get their both;

dates=w.tdays(dateStart,yesterday).Data[0]

opens=w.wsd(stocksAdd,'open',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
closes=w.wsd(stocksAdd,'close',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
highs=w.wsd(stocksAdd,'high',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
lows=w.wsd(stocksAdd,'low',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
vols=w.wsd(stocksAdd,'volume',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
turns=w.wsd(stocksAdd,'free_turn',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
Lt=len(stocksAdd)
for i in range(Lt):
    print('add stock-%s %d/%d;' %(stocksAdd[i],i+1,Lt))
    try:
        tem=np.isnan(opens[i]).sum() #for none value pandas.isnull can treate it;
    except:
        continue                
    Matrix=[dates[tem:],opens[i][tem:],closes[i][tem:],highs[i][tem:],lows[i][tem:],vols[i][tem:],turns[i][tem:]]
    cur.execute('create table if not exists '+stocksAdd[i][:6]+stocksAdd[i][7:]+'(date date,open float,close float,high float,low float,vol bigint,turn float)')
    cur.executemany('insert into '+stocksAdd[i][:6]+stocksAdd[i][7:]+' values(%s,%s,%s,%s,%s,%s,%s)', np.column_stack(Matrix).tolist()) 
cur.executemany('insert into stocks values(%s)', stocksAdd)

opens=[]
closes=[]
highs=[]
lows=[]
vols=[]
turns=[]
Lt=len(stocksRaw)
for i in range(0,Lt,400):
    if i+400>Lt:
        iend=Lt
    else:
        iend=i+400
    while 1:
        tem=w.wsd(stocksRaw[i:iend],'open',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
        if type(tem[0][0])==float:
            if len(tem)>1:
                opens.extend(tem)
            else:
                opens.extend(tem[0])
            break
    while 1:
        tem=w.wsd(stocksRaw[i:iend],'close',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
        if type(tem[0][0])==float:
            if len(tem)>1:
                closes.extend(tem)
            else:
                closes.extend(tem[0])
            break
    while 1:
        tem=w.wsd(stocksRaw[i:iend],'high',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
        if type(tem[0][0])==float:
            if len(tem)>1:
                highs.extend(tem)
            else:
                highs.extend(tem[0])
            break
    while 1:
        tem=w.wsd(stocksRaw[i:iend],'low',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
        if type(tem[0][0])==float:
            if len(tem)>1:
                lows.extend(tem)
            else:
                lows.extend(tem[0])
            break
    while 1:
        tem=w.wsd(stocksRaw[i:iend],'volume',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
        if type(tem[0][0])==float:
            if len(tem)>1:
                vols.extend(tem)
            else:
                vols.extend(tem[0])
            break
    while 1:
        tem=w.wsd(stocksRaw[i:iend],'free_turn',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
        if type(tem[0][0])==float:
            if len(tem)>1:
                turns.extend(tem)
            else:
                turns.extend(tem[0])
            break
for i in range(Lt):
    print('update stock %d/%d;' %(i+1,Lt))
    if len(dates)==1:
        temCheck=opens[i]
        if type(temCheck)==float:
            if str(temCheck)[0].isdigit():
                Matrix=np.column_stack([dates[0],opens[i],closes[i],highs[i],lows[i],vols[i],turns[i]]).tolist()
            else:
                tem=cur.execute('select * from '+stocksRaw[i][:6]+stocksRaw[i][7:])
                cur.scroll(tem-1,'absolute')
                tem=cur.fetchone()
                Matrix=[list(tem)]
                Matrix[0][0]=yesterday
                Matrix[0][5]=0
                Matrix[0][6]=0.0
        else:
            print('the day is not trading day; no need to update database!')
            cur.close()
            conn.close()        
    else:
        temChar=str(opens[i][0])[0]
        if temChar.isdigit():
            Matrix=np.column_stack([dates,opens[i],closes[i],highs[i],lows[i],vols[i],turns[i]]).tolist()
        elif temChar.lower()=='n':
            tem=cur.execute('select * from '+stocksRaw[i][:6]+stocksRaw[i][7:])
            cur.scroll(tem-1,'absolute')
            tem=cur.fetchone()
            Matrix=np.tile(tem,[len(dates),1]).tolist()
        else:
            cur.close()
            conn.close()
    cur.executemany('insert into '+stocksRaw[i][:6]+stocksRaw[i][7:]+' values(%s,%s,%s,%s,%s,%s,%s)', Matrix) 