stock=['600000','300001','000001','000002','000004','000005']
targetPrice=[12.71,0.3,0.3,0.3,0.3,0.3]
while 1:
    time.sleep(1)
    priceCurrent=list(map(float,ts.get_realtime_quotes(stock)['price']))
    timeStr=time.strftime('%H:%M:%S', time.localtime())
    msgRecord=[]
    for i in range(len(stock)):
        if targetPrice[i]>0:
            if priceCurrent[i]>targetPrice[i]:
                msgRecord.append(timeStr+' stock '+stock[i]+' 已大于目标点位。')
            else:
                print(timeStr+ 'stock '+stock[i]+' 还差'+str(round(targetPrice[i]-priceCurrent[i],3))+'个点，才能到达目标点位。')
        else:
            if priceCurrent[i]<-targetPrice[i]:
                msgRecord.append(timeStr + ' stock ' + stock[i] + ' 已小于目标点位。')
            else:
                print(timeStr+' stock '+stock[i]+' 还差'+str(round(targetPrice[i]+priceCurrent[i],3))+'个点，才能到达目标点位。')
    if len(msgRecord):
        tmp='\n'.join(msgRecord)
        tmp = win32api.MessageBox(0, tmp, 'Alert!', 1)
        if tmp==1:
            print('Monitor continues!')
        else:
            print('Monitor exits!')
            break




