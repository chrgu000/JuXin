import tushare as ts
import numpy as np
import win32api
import time

stock=['600000','300001','000001','000002','000004','000005'] #被检测的标的（股票/指数）
targetPrice=[12.71,0.3,0.3,0.3,0.3,0.3] #对应每个标的被检测的报警价格，注：正值表示标的价格大于该值时报警，负值表示标的价格小于该值时报警；
while 1:
    time.sleep(1) #每隔一秒获取一次
    priceCurrent=list(map(float,ts.get_realtime_quotes(stock)['price'])) #获取所有标的实时价格
    timeStr=time.strftime('%H:%M:%S', time.localtime()) #获取当前时间字符串
    msgRecord=[] #记录需要报警的信息
    for i in range(len(stock)):
        if targetPrice[i]>0:
            if priceCurrent[i]>targetPrice[i]: #当价格超过预设值时，弹出报警信息
                msgRecord.append(timeStr+' stock '+stock[i]+' 已大于目标点位。')
            else: #如果没到，则在终端显示还差多少点到达预设值；
                print(timeStr+ 'stock '+stock[i]+' 还差'+str(round(targetPrice[i]-priceCurrent[i],3))+'个点，才能到达目标点位。')
        else:
            if priceCurrent[i]<-targetPrice[i]: #当价格下跌跌过预设值时，弹出报警信息；
                msgRecord.append(timeStr + ' stock ' + stock[i] + ' 已小于目标点位。')
            else: #如果没到，则在终端显示还差多少点到达预设值
                print(timeStr+' stock '+stock[i]+' 还差'+str(round(targetPrice[i]+priceCurrent[i],3))+'个点，才能到达目标点位。')
    if len(msgRecord): #如果有报警信息，调用win32api弹出对话框
        tmp='\n'.join(msgRecord)
        tmp = win32api.MessageBox(0,tmp, 'Alert!', 1)
        if tmp==1:
            print('Monitor continues!')
        else:
            print('Monitor exits!')
            break




