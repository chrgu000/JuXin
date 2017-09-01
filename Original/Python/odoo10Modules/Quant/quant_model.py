# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions
from openerp import tools

from WindPy import *
#  from mlab.releases import latest_release as matlab
import matlab.engine, base64, io, os, re, Image, StringIO, datetime, math #,openpyxl,os,xlrd,time
import pandas as pd
import numpy as np
import matplotlib.finance as mpf
import tushare as ts
from sklearn.linear_model import LinearRegression
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt


import sys # kick  ascii code errors
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

from pylab import *  # for Chinese charactors
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

class QuantTask(models.Model):
    _name = 'quant.task'
    _description = 'Quant task'
    name = fields.Char()
    data=fields.Binary(u'数据下载（需将扩展名改为xlsx）')
    startTime=fields.Date(u'开始时间', default='2016-01-01')
    endTime=fields.Date(u'结束时间', default=fields.Date.today())
    selectStocks=fields.Html(u'股票代码  （若需添加多个股票，用逗号隔开如：000001,600000；若不填加任何股票，默认下载所有股票）')
    indexButton=fields.Boolean(u'指数？')

    @api.multi
    def getData(self,cr):
        self.name=self.env.user.name +'修改于：'+ fields.Date.today()
        #uidTem=cr[u'uid']
        #self.name=self.env['res.users'].browse(uidTem).name
        drTem = re.compile(r'<[^>]+>', re.S)
        testTem = drTem.sub('', self.selectStocks)
        if testTem!='':
            stocks=testTem.split(',')
        else:
            dataRaw = ts.get_stock_basics()
            stocks = dataRaw.index
        #stocks = stocks[0:2]

        numStocks = len(stocks)
        dataTem = ts.get_k_data('000001', index=True,start=self.startTime,end=self.endTime)
        Lall = len(dataTem)
        dataOpen = pd.DataFrame(columns=stocks, index=np.arange(Lall))
        dataHigh = pd.DataFrame(columns=stocks, index=np.arange(Lall))
        dataLow = pd.DataFrame(columns=stocks, index=np.arange(Lall))
        dataClose = pd.DataFrame(columns=stocks, index=np.arange(Lall))
        dataVolume = pd.DataFrame(columns=stocks, index=np.arange(Lall))
        for i in range(numStocks):
            dataTem = ts.get_k_data(stocks[i],index=self.indexButton,start=self.startTime,end=self.endTime)
            dataOpen.iloc[:, i] = dataTem.iloc[:, 1]
            dataClose.iloc[:, i] = dataTem.iloc[:, 2]
            dataHigh.iloc[:, i] = dataTem.iloc[:, 3]
            dataLow.iloc[:, i] = dataTem.iloc[:, 4]
            dataVolume.iloc[:, i] = dataTem.iloc[:, 5]
        #fileTem = 'D:\%s.xlsx' % cr['uid']
        fileTem = StringIO.StringIO()
        writerTem = pd.ExcelWriter(fileTem, engine='xlsxwriter')
        dataOpen.to_excel(writerTem, 'Open')
        dataClose.to_excel(writerTem, 'Close')
        dataHigh.to_excel(writerTem, 'High')
        dataLow.to_excel(writerTem, 'Low')
        dataVolume.to_excel(writerTem, 'Volume')
        writerTem.save()
        self.write({'data': base64.encodestring(fileTem.getvalue())})
        #tem = open(fileTem, 'rb')
        #self.write({'data': tem.read().encode('base64')})
        #tem.close()
        #os.remove(fileTem)


class PlotTask(models.Model):
    _name = 'plot.task'
    _description = 'Plot task'
    name = fields.Char()
    stock=fields.Char(u'股票代码', size=9 , required=True,help=u'必须九位数，如000001.SH,300001.SZ等')
    #indexButton = fields.Boolean(u'指数？')
    notes=fields.Html(u'运行情况')
    wd = fields.Boolean(u'周交易日', default=True)
    md = fields.Boolean(u'月交易日')
    m = fields.Boolean(u'交易月')
    lmd = fields.Boolean(u'阴历交易日')
    lm = fields.Boolean(u'阴历交易月')
    s = fields.Boolean(u'二十四节气')
    wdP = fields.Binary()
    mdP = fields.Binary()
    mP = fields.Binary()
    lmdP = fields.Binary()
    lmP = fields.Binary()
    sP = fields.Binary()

    @api.multi
    def selectAll(self):
        self.wd = True
        self.md = True
        self.m = True
        self.lmd = True
        self.lm = True
        self.s = True

    def plotP(self,indTem,data,name,pic,xTicks):
        aa = [x[indTem] for x in data ]
        Aa = [x[indTem + 1] for x in data]
        F = [x[indTem + 2] for x in data[0:2]]
        plt.figure(figsize=(8.2, 6))
        xPoints = data.size[0]+1
        xTem = range(xPoints )[1:xPoints]
        plt.bar(xTem, aa, width=0.35, facecolor='lightskyblue', edgecolor='white', label='aa')
        xTem = [x + 0.35 for x in xTem]
        plt.bar(xTem, Aa, width=0.35, facecolor='yellowgreen', edgecolor='white', label='Aa')
        plt.text(1, max(aa) * 1.02, name + '统计---F值:%.2f;Prob>F:%.2f' % (F[0], F[1]))
        plt.xticks(xTem, xTicks,rotation=60)
        #plt.xticks(xTem,[r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
        picData = StringIO.StringIO()
        plt.savefig(picData)
        self.write({pic: base64.encodestring(picData.getvalue())})
        #pic_data = open(pathname, 'rb').read()
        #self.write({pic: base64.encodestring(pic_data)})

    @api.multi
    def figplot(self,cr):
        print "test.............................."
        x=tools.email_send(email_from='116599778@qq.com',
                         email_to=['568588@qq.com'],
                         subject='Some subject just a test',
                         body='Some body', )
        print x
        print "tested....................................."
        self.name = self.env.user.name +'修改于：'+ fields.Date.today()
        self.notes=''
        if len(self.stock)<9:
            self.notes='股票代码错误，代码位数小于9！'
            self.wdP = ''
            self.mdP = ''
            self.mP = ''
            self.lmdP = ''
            self.lmP = ''
            self.sP = ''
            return
        Meng = matlab.engine.start_matlab()
        typeX=''
        if self.wd:
            typeX +='wd'
            if self.md:
                typeX += ',md'
            if self.m:
                typeX += ',m'
            if self.lmd:
                typeX += ',lmd'
            if self.lm:
                typeX += ',lm'
            if self.s:
                typeX += ',s'
        try:
            data= Meng.pyWDM(self.stock,typeX, 2, nargout=1)
        except:
            self.notes = '未获取到股票数据，可能原因为:代码输入错误或者windmatlab错误等！'
            self.wdP = ''
            self.mdP = ''
            self.mP = ''
            self.lmdP = ''
            self.lmP = ''
            self.sP = ''
            return
        indTem=0
        #pathTem = 'D:\%s.png' % cr['uid']
        if self.wd:
            try:
                xTicks=['周一','周二','周三','周四','周五']
                self.plotP(indTem,data[0:5], '周交易日','wdP',xTicks)
            except:
                self.notes += '数据获取成功，‘周交易日’作图失败，原因可能为：可用有效数据量太少！'
                self.wdP = ''
            indTem += 3
        if self.md:
            try:
                xTicks = ['1号','2号','3号','4号','5号','6号','7号','8号','9号','10号','11号','12号','13号','14号','15号',\
                          '16号','17号','18号','19号','20号','21号','22号','23号','24号','25号','26号','27号','28号','29号','30号','31号']
                self.plotP(indTem, data[0:31], '月交易日', 'mdP', xTicks)
            except:
                self.notes += '数据获取成功，‘月交易日’作图失败，原因可能为：可用有效数据量太少！'
                self.mdP = ''
            indTem += 3
        if self.m:
            try:
                xTicks = ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
                self.plotP(indTem, data[0:12], '交易月','mP',xTicks)
            except:
                self.notes += '数据获取成功，‘交易月’作图失败，原因可能为：可用有效数据量太少！'
                self.mP = ''
            indTem += 3
        if self.lmd:
            try:
                xTicks = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十', '十一', '十二', '十三', '十四', '十五', '十六', \
                          '十七', '十八', '十九', '二十', '二十一', '二十二', '二十三', '二十四', '二十五', '二十六', '二十七', '二十八', '二十九', '三十', '三十一']
                self.plotP(indTem, data[0:30], '阴历交易日','lmdP',xTicks)
            except:
                self.notes += '数据获取成功，‘阴历交易日’作图失败，原因可能为：可用有效数据量太少！'
                self.lmdP = ''
            indTem += 3
        if self.lm:
            try:
                xTicks = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
                self.plotP(indTem, data[0:12], '阴历交易月','lmP',xTicks)
            except:
                self.notes += '数据获取成功，‘阴历交易月’作图失败，原因可能为：可用有效数据量太少！'
                self.lmP = ''
            indTem += 3
        if self.s:
            try:
                xTicks=['大寒','小寒','立春','雨水','惊蛰','春分','清明','谷雨','立夏','小满','芒种','夏至','小暑',\
                        '大暑','立秋','处暑','白露','秋分','寒露','霜降','立冬','小雪','大雪','冬至','其它']
                self.plotP(indTem, data[0:25], '二十四节气','sP',xTicks)
            except:
                self.notes += '数据获取成功，‘二十四节气’作图失败，原因可能为：可用有效数据量太少！'
                self.sP = ''
            indTem += 3
        if indTem > 0 and self.notes=='':
            self.notes = '程序运行正常，统计已完成！'


class ColorTask(models.Model):
    _name = 'color.task'
    _description = 'Color task'
    datafile = fields.Binary(u'请选择图片', required=True)
    redvalue = fields.Float(u'色价量化值')

    @api.multi
    def colorread(self, cr):
        file_like = io.BytesIO(base64.b64decode(self.datafile))
        im = Image.open(file_like)
        width = im.size[0]
        length = im.size[1]
        value = 0.0
        for i in range(0, width):
            for j in range(0, length):
                value = value + im.getpixel((i, j))[0]
        value = value / (i * j)
        self.redvalue = value / 255

class HedgeHS300(models.Model):
    _name = 'monthhedge'
    _inherit = ['mail.thread']
    _description = 'Month Hedge'
    #_order = "id desc"

    name = fields.Char(default='正在创建...')
    picture = fields.Binary('策略测试走势图')
    currentMonth = fields.Integer('当前月份：',default=-1)
    stocksHold = fields.Html('当前持股情况：')

    @api.multi
    def getResult(self,cr):
        #print self.id
        w.start()
        if w.tdays().ErrorCode != 0:
            return
        self.name = '由 '+self.env.user.name + ' 更新于：' + \
                    datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(hours=8),'%Y%m%d %H:%M:%S')
        testTem = pd.read_excel('D:\Trading\WFT\hs300hedgeResults.xlsx', header=None)
        testTemCopy = pd.read_excel('D:\Trading\WFT\hs300hedgeResultsCopy.xlsx', header=None)
        if len(testTem) >= len(testTemCopy):
            os.system("copy D:\Trading\WFT\hs300hedgeResults.xlsx D:\Trading\WFT\hs300hedgeResultsCopy.xlsx")
        else:
            os.system("copy D:\Trading\WFT\hs300hedgeResultsCopy.xlsx D:\Trading\WFT\hs300hedgeResults.xlsx")
        writer = pd.ExcelWriter('D:\Trading\WFT\hs300hedgeResults.xlsx', engine='xlsxwriter')
        if self.currentMonth<1:
            self.currentMonth = datetime.date.today().month
            dateNow = datetime.datetime.strftime(datetime.date.today(), '%Y%m%d')
            pd.DataFrame([dateNow]).to_excel(writer, sheet_name='date', columns=None, index=None, header=None)
            stocks = pd.read_excel('D:\Trading\WFT\\topNStocks.xlsx', header=None)
            stocksTem = stocks.loc[self.currentMonth - 1, :].tolist()
            self.stocksHold = '买入：\n'+'\n'.join(stocksTem)+'\n'+'卖出：'+'\n'+'000300.SH'
            stocksCurrent = self.stocksHold.split('\n')[1:-2]
            priceTem=pd.DataFrame(w.wsq(stocksCurrent, "rt_latest").Data[0])
            priceTem300=pd.DataFrame(w.wsq('000300.sh', "rt_latest").Data[0])
            priceTem.append(priceTem300).to_excel(writer, sheet_name='priceLast',columns=None, index=None, header=None)
            pd.DataFrame([1]).to_excel(writer, sheet_name='results',columns=None, index=None, header=None)
            pd.DataFrame([1]).to_excel(writer, sheet_name='HS300results', columns=None, index=None, header=None)
            writer.save()
            #self.daysList.append(datetime.date.today())
            #self.currentStocks=stocks.loc[self.currentMonth-1,:].tolist()
            #self.startClose=np.array(w.wsq(self.currentStocks, "rt_latest").Data[0])
            #self.startHS300=np.array(w.wsq('000300.sh', "rt_latest").Data[0])
            #self.results.append(0.0)
        else:
            stocksCurrent=self.stocksHold.split('\n')[1:-2]
            try:
                currentClose = pd.DataFrame(w.wsq(stocksCurrent, "rt_latest").Data[0])
                currentHS300 = pd.DataFrame(w.wsq('000300.sh', "rt_latest").Data[0])
            except Exception as err:
                print err
                print 'w.wsq has some error!'
                return
            datePast=pd.read_excel('D:\Trading\WFT\hs300hedgeResults.xlsx','date',header=None)
            priceLast = pd.read_excel('D:\Trading\WFT\hs300hedgeResults.xlsx', 'priceLast',header=None)
            resultsPast=pd.read_excel('D:\Trading\WFT\hs300hedgeResults.xlsx','results',header=None)
            HS300ResultsPast = pd.read_excel('D:\Trading\WFT\hs300hedgeResults.xlsx', 'HS300results', header=None)
            dateCurrent = datetime.datetime.strftime(datetime.date.today(), '%Y%m%d')
            if self.currentMonth in [1,6,8]:
                self.stocksHold = '买入：\n' + 'None' + '\n' + '卖出：' + '\n' + '000300.SH'
                stocksCurrent=['000001.sh']
                closeParameter=0
                HS300Parameter=0.5
            else:
                closeParameter = 1
                HS300Parameter = 0
            if self.currentMonth == datetime.date.today().month:
                returnClose = currentClose / priceLast[:-1] - 1
                returnHS300 = 1 - currentHS300 / priceLast.iloc[-1]
                returnAll = closeParameter * returnClose.mean() + HS300Parameter * returnHS300
                if str(datePast[0].tolist()[-1]) != dateCurrent:
                    dateUpdate=datePast.append(pd.DataFrame([dateCurrent]))
                    dateUpdate.to_excel(writer, sheet_name='date', columns=None, index=None, header=None)
                    resultsUpdate = resultsPast.append((returnAll + 1) * resultsPast.iloc[-1])
                    resultsUpdate.to_excel(writer, sheet_name='results', columns=None, index=None, header=None)
                    print HS300ResultsPast
                    print returnHS300
                    HS300ResultsUpdate= HS300ResultsPast.append((1-returnHS300)*HS300ResultsPast.iloc[-1])
                    print HS300ResultsUpdate

                    HS300ResultsUpdate.to_excel(writer, sheet_name='HS300results', columns=None, index=None, header=None)
                    currentClose.append(currentHS300).to_excel(writer, sheet_name='priceLast', columns=None, index=None,
                                                               header=None)
                    writer.save()
                else:
                    print HS300ResultsPast
                    print returnHS300
                    resultTem = (1 + returnAll) * resultsPast.iloc[-1]
                    HS300ResultTem = (1 - returnHS300) * HS300ResultsPast.iloc[-1]
                    resultsPast.iloc[-1] = resultTem.iloc[0]
                    HS300ResultsPast.iloc[-1] = HS300ResultTem.iloc[0]
                    print HS300ResultsPast

                    resultsUpdate = resultsPast
                    resultsUpdate.to_excel(writer, sheet_name='results', columns=None, index=None, header=None)
                    HS300ResultsUpdate = HS300ResultsPast
                    HS300ResultsUpdate.to_excel(writer, sheet_name='HS300results', columns=None, index=None,
                                                header=None)
                    currentClose.append(currentHS300).to_excel(writer, sheet_name='priceLast', columns=None, index=None,
                                                               header=None)
                    dateUpdate = datePast
                    dateUpdate.to_excel(writer, sheet_name='date', columns=None, index=None, header=None)
                    writer.save()
            else:
                self.currentMonth = datetime.date.today().month
                dataTem = w.wsd('000001.sh', 'close', 'ED-20TD')
                dataS = dataTem.Times
                monthS = [dataS[i].month for i in range(len(dataS))]
                indTarget = monthS.index(self.currentMonth) - 1
                dayTarget = dataS[indTarget]
                stocks = pd.read_excel('D:\Trading\WFT\\topNStocks.xlsx', header=None)
                stocksPast = stocks.loc[self.currentMonth - 2, :].tolist()
                stocksTem = stocks.loc[self.currentMonth - 1, :].tolist()
                self.stocksHold = '买入：\n' + '\n'.join(stocksTem) + '\n' + '卖出：' + '\n' + '000300.SH'
                stocksCurrent = self.stocksHold.split('\n')[1:-2]
                tradeDateLast = 'tradeDate=' + datetime.date.strftime(dayTarget, '%Y%m%d')
                pastClose = pd.DataFrame(w.wss(stocksPast, 'close', tradeDateLast, 'priceAdj=F', 'cycle=D').Data[0])
                pastHS300 = pd.DataFrame(w.wss('000300.sh', 'close', tradeDateLast, 'priceAdj=F', 'cycle=D').Data[0])
                if self.currentMonth-1 in [1, 6, 8]:
                    closeParameterLast = 0.5
                    HS300ParameterLast = 0.5
                else:
                    closeParameterLast = 1
                    HS300ParameterLast = 0
                returnClosePast = pastClose / priceLast[:-1] - 1
                returnHS300Past = 1 - pastHS300 / priceLast.iloc[-1]
                returnAllPast = closeParameterLast * returnClosePast.mean()+ HS300ParameterLast * returnHS300Past

                resultTem = (returnAllPast + 1) * resultsPast.iloc[-1]
                HS300ResultTem = (1 - returnHS300Past) * HS300ResultsPast.iloc[-1]
                startClose = pd.DataFrame(w.wss(stocksCurrent, 'close', tradeDateLast, 'priceAdj=F', 'cycle=D').Data[0])
                startHS300 = pd.DataFrame(w.wss('000300.sh', 'close', tradeDateLast, 'priceAdj=F', 'cycle=D').Data[0])
                currentClose = pd.DataFrame(w.wsq(stocksCurrent, "rt_latest").Data[0])
                returnClose = currentClose / startClose - 1
                returnHS300 = 1 - currentHS300 / startHS300
                returnAll = closeParameter * returnClose.mean() + HS300Parameter * returnHS300
                resultPlus = resultTem * (1 + returnAll)
                HS300ResultPlus = HS300ResultTem * (1 - returnHS300)

                dateUpdate=datePast.append(pd.DataFrame([dateCurrent]))
                dateUpdate.to_excel(writer, sheet_name='date', columns=None, index=None, header=None)
                resultsUpdate = resultsPast.append(resultPlus)
                resultsUpdate.to_excel(writer, sheet_name='results', columns=None, index=None, header=None)
                HS300ResultsUpdate = HS300ResultsPast.append(HS300ResultPlus)
                HS300ResultsUpdate.to_excel(writer, sheet_name='HS300results', columns=None, index=None, header=None)
                currentClose.append(currentHS300).to_excel(writer, sheet_name='priceLast', columns=None, index=None,
                                                           header=None)


            plt.figure(figsize=(15, 6))
            lengthTem = len(resultsUpdate)
            plt.plot(range(1, lengthTem + 1), resultsUpdate, label="策略实时回测曲线")
            plt.plot(range(1, lengthTem + 1), HS300ResultsUpdate, label="沪深300指数实时走势曲线")
            xTicks = [dateUpdate.iloc[i].tolist()[0] for i in range(lengthTem)]
            plt.xticks(range(1, lengthTem + 1), xTicks, rotation=60)
            plt.legend(loc='upper left', bbox_to_anchor=(0.01,1.1),ncol=2,fancybox=True,shadow=True)
            plt.grid()
            picData = StringIO.StringIO()
            plt.savefig(picData)
            self.write({'picture': base64.encodestring(picData.getvalue())})

class HedgeCH(models.Model):
    _name = 'hedgech'
    _description = 'IC VS IH'
    _inherit = ['mail.thread']

    name = fields.Char(default='CvsH')
    picture = fields.Binary('策略测试走势图')
    date = fields.Text('测试日期')
    results0 = fields.Text('测试完全对冲结果')
    results1 = fields.Text('测试实际对冲结果')

    @api.multi
    def getResult(self, cr):
        w.start()
        if w.tdays().ErrorCode != 0:
            return
        today=datetime.date.strftime( datetime.date.today(),'%Y%m%d')
        if self.date==False:
            self.date=today
            self.results0=''
            self.results1=''
        else:
            result0list = self.results0.split(',')
            result1list = self.results1.split(',')
            datelist=self.date.split(',')
            tem=w.tdays(datelist[-1], today)
            tem=len(tem.Times)
            tem='ED-'+str(tem)+'TD'
            data = w.wsd('ic.cfe,ih.cfe', 'pct_chg', tem)
            closeP = w.wsd('ic.cfe,ih.cfe', 'close', tem)
            closeP=pd.DataFrame(closeP.Data)
            weights0=closeP.loc[0]*2/(closeP.loc[0]*2+closeP.loc[1]*6)
            weights1=1-weights0
            dateTem=data.Times
            pctchg=pd.DataFrame(data.Data)/100
            datanow=w.wsq('ic.cfe,ih.cfe', 'rt_pct_chg')
            pctchg.iloc[:,-1]=datanow.Data[0]
            diffTem=pctchg.loc[0]-pctchg[1]
            weekTem=[dateTem[i].weekday()+1 for i in range(len(dateTem))]
            for i in range(len(diffTem)-1):
                wd=weekTem[i+1]
                temLast=diffTem[i]
                resultTem0=pctchg.iloc[0,i+1]-pctchg.iloc[1,i+1]
                resultTem1=pctchg.iloc[0,i+1]*weights0[i]-pctchg.iloc[1,i+1]*weights1[i]
                if wd==1:
                    if temLast>=-0.0180 and temLast<=0.0279 :
                        result0Tem = -resultTem0
                        result1Tem = -resultTem1
                    elif temLast<0.037:
                        result0Tem = resultTem0
                        result1Tem = resultTem1
                    else:
                        result0Tem = 0
                        result1Tem = 0
                if wd==2:
                    if temLast>=-0.05 and temLast<=0.075:
                        result0Tem = resultTem0
                        result1Tem = resultTem1
                    else:
                        result0Tem = -resultTem0
                        result1Tem = -resultTem1
                if wd==3:
                    if temLast>=-0.006:
                        result0Tem = -resultTem0
                        result1Tem = -resultTem1
                    else:
                        result0Tem = resultTem0
                        result1Tem = resultTem1
                if wd==4:
                    if temLast>=-0.065:
                        result0Tem = resultTem0
                        result1Tem = resultTem1
                    else:
                        result0Tem = -resultTem0
                        result1Tem = -resultTem1
                if wd==5:
                    if temLast>=0.031:
                        result0Tem = -resultTem0
                        result1Tem = -resultTem1
                    else:
                        result0Tem = resultTem0
                        result1Tem = resultTem1
                    result0Tem=0 # --------------------------------------------------no trades on Friday;
                    result1Tem=0

                if i==0:
                    if float(result0list[-1]) >= -0.011: #--------------------------------------------last modified;
                        print 'test2'
                        if result0Tem >-0.011:
                            result0list[-1] = str(result0Tem)
                            result1list[-1] = str(result1Tem)
                        else:
                            result0list[-1] = str(-0.012)
                            result1list[-1] = str(-0.012)
                        datelist[-1] = datetime.date.strftime(dateTem[i + 1], '%Y%m%d')
                    #result0list[-1] = str(result0Tem) #----------------------------before modified;
                    #result1list[-1] = str(result1Tem)
                    #datelist[-1]=datetime.date.strftime(dateTem[i+1],'%Y%m%d')
                else:
                    if result0Tem >= -0.011:  # --------------------------------------------last modified;
                        result0list.append(str(result0Tem))
                        result1list.append(str(result1Tem))
                    else:
                        result0list.append(str(-0.011))
                        result1list.append(str(-0.011))
                    datelist.append(datetime.date.strftime(dateTem[i + 1], '%Y%m%d'))
                    #result0list.append(str(result0Tem)) #--------------------------before modified
                    #result1list.append(str(result1Tem))
                    #datelist.append(datetime.date.strftime(dateTem[i+1],'%Y%m%d'))

            self.date=','.join(datelist)
            self.results0=','.join(result0list)
            self.results1 = ','.join(result1list)
            result0num=[float(result0list[i]) for i in range(len(result0list))]
            result0sum=[sum(result0num[0:i+1]) for i in range(len(result0num))]
            result1num = [float(result1list[i]) for i in range(len(result1list))]
            result1sum = [sum(result1num[0:i + 1]) for i in range(len(result1num))]
            plt.figure(figsize=(15, 6))
            lengthTem = len(result0num)
            plt.plot(range(1, lengthTem + 1), result0sum, label="策略完全对冲实时测试")
            plt.plot(range(1, lengthTem + 1), result1sum, label="策略实际对冲实时测试")
            #xTicks = [dateUpdate.iloc[i].tolist()[0] for i in range(lengthTem)]
            plt.xticks(range(1, lengthTem + 1), datelist, rotation=60)
            plt.legend(loc='upper left', bbox_to_anchor=(0.01, 1.1), ncol=2, fancybox=True, shadow=True)
            linreg=LinearRegression()
            Ltem=len(result0sum)
            sumInd=[[i] for i in range(Ltem)]
            sum01=[[result0sum[i],result1sum[i]] for i in range(Ltem)]
            linreg.fit(sumInd,sum01)
            beta = linreg.coef_.round(3).tolist()
            beta = 'Beta：' + str(beta[0][0]) + '/' + str(beta[1][0]) + '; '
            residues = linreg.residues_.round(3).tolist()
            residues = '残差：' + str(residues[0]) + '/' + str(residues[1]) + '; '
            result0DF = pd.DataFrame(result0num)
            sharpe0=(result0DF.mean()/result0DF.std()).round(2)
            sharpe0= str(sharpe0.tolist()[0])
            result1DF = pd.DataFrame(result1num)
            sharpe1 = (result1DF.mean() / result1DF.std()).round(2)
            sharpe1 = str(sharpe1.tolist()[0])
            sharpe = 'Sharpe：' + sharpe0 + '/' + sharpe1
            plt.figtext(0.41, 0.91, beta + residues + sharpe, color='red', ha='left', fontsize=12, fontweight='bold',alpha=0.8,\
                        bbox={'facecolor': 'gray', 'alpha': 0.5, 'pad': 0.3,'edgecolor':'None','boxstyle':'round'},rotation="horizontal")#transform=trans,
            plt.grid()
            picData = StringIO.StringIO()
            plt.savefig(picData)
            self.write({'picture': base64.encodestring(picData.getvalue())})
            print self.date
            print self.results0
            print self.results1


class HedgeZnM(models.Model):
    _name = 'hedgeznm'
    _description = 'Trade Zn in minutes'
    _inherit = ['mail.thread']

    tradeNum = fields.Text('每个交易日交易次数')
    name = fields.Char(default='trade Zn')
    pictureZn = fields.Binary('锌策略测试')
    dateZn = fields.Text('锌交易日期')
    resultsZnP = fields.Text('锌以前结果')
    dateZnNew = fields.Text('新锌交易日期')
    resultsZnPNew = fields.Text('新锌以前结果')

    pictureRu = fields.Binary('橡胶策略测试')
    dateRu = fields.Text('橡胶交易日期')
    resultsRuP = fields.Text('橡胶以前结果')
    dateRuNew = fields.Text('新橡胶交易日期')
    resultsRuPNew = fields.Text('新橡胶以前结果')

    pictureWh = fields.Binary('强麦策略测试')
    dateWh = fields.Text('强麦交易日期')
    resultsWhP = fields.Text('强麦以前结果')

    pictureM = fields.Binary('豆粕策略测试')
    dateM = fields.Text('豆粕交易日期')
    resultsMP = fields.Text('豆粕以前结果')

    @api.multi
    def getResult(self, cr):
        w.start()
        if w.tdays().ErrorCode != 0:
            return
        today = datetime.date.today()
        todayT = datetime.date.strftime(today, '%Y%m%d')
        startDay = datetime.date.today() - datetime.timedelta(days=2)
        startDayT = datetime.date.strftime(startDay, '%Y%m%d')

        #新锌交易情况
        if self.dateZnNew == False:
            data=w.wsi('zn.shf','close',startDayT+' 09:00:00',todayT+' 15:01:00',\
                   'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        else:
            datePast = self.dateZnNew.split(',')
            data = w.wsi('zn.shf', 'close', datePast[-1] + ' 09:00:00', todayT + ' 15:01:00', \
                         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        Points = data.Data[0]
        Dates = data.Times
        ResultT = -1
        DateT=-1
        L = len(Points)
        if L <5:
            return
        else:
            if L % 226 ==0:
                loop = L/226
            else:
                loop = L/226 +1

        for i in range(loop):
            if L<(i+1)*226:
                endi = L
            else:
                endi = (i+1)*226
            if endi-226 <0:
                starti = 0
            else:
                starti = (i)*226
            points=Points[starti:endi]
            lengthP = len(points)
            if lengthP > 5:
                resultT=-1
                dateT = datetime.date.strftime(Dates[i*226], '%Y%m%d')
                wd = Dates[i*226].weekday() + 1
                if wd == 1:
                    resultT = 0
                elif wd == 2:
                    if lengthP >79:
                        resultT = points[68] / points[79] + points[68] / points[60] + points[25] / points[44] - 3
                    elif lengthP >68:
                        resultT = points[68] / points[-1] + points[68] / points[60] + points[25] / points[44] - 3
                    elif lengthP >60:
                        resultT = points[-1] / points[60] + points[25] / points[44] - 2
                    elif lengthP >44:
                        resultT = points[25] / points[44] - 1
                    elif lengthP >25:
                        resultT = points[25] / points[-1] - 1
                elif wd == 3:
                    if lengthP >107:
                        resultT = points[97] / points[107] + points[55] / points[62] - 2
                    elif lengthP >97:
                        resultT = points[97] / points[-1] + points[55] / points[62] - 2
                    elif lengthP >62:
                        resultT = points[55] / points[62] - 1
                    elif lengthP >55:
                        resultT = points[55] / points[-1] - 1
                elif wd == 4:
                    if lengthP >149:
                        resultT = points[149] / points[143] + points[85] / points[79] + points[74] / points[79] - 3
                    elif lengthP >143:
                        resultT = points[-1] / points[143] + points[85] / points[79] + points[74] / points[79] - 3
                    elif lengthP >85:
                        resultT = points[85] / points[79] + points[74] / points[79] - 2
                    elif lengthP >79:
                        resultT = points[-1] / points[79] + points[74] / points[79] - 2
                    elif lengthP >74:
                        resultT = points[74] / points[-1] - 1
                elif wd == 5:
                    resultT = 0

                if resultT != -1:
                    if ResultT == -1:
                        ResultT = [resultT]
                        DateT = [dateT]
                    else:
                        ResultT.append(resultT)
                        DateT.append(dateT)
        if ResultT == -1:
            return
        if self.resultsZnPNew == False:
            resultsDraw = ResultT
            dateDraw = DateT
        else:
            resultsDraw = map(eval,self.resultsZnPNew.split(','))[0:-1] + ResultT
            dateDraw = self.dateZnNew.split(',')[0:-1] + DateT
        self.dateZnNew =  ','.join(dateDraw)
        self.resultsZnPNew = ','.join(map(str,resultsDraw))

        plt.figure(figsize=(15, 6))
        lengthTem = len(resultsDraw)
        resultsArray = np.array(resultsDraw)
        resultsCum = resultsArray.cumsum()
        plt.plot(range(1, lengthTem + 1), resultsCum, label="新锌测试")
        # xTicks = [dateUpdate.iloc[i].tolist()[0] for i in range(lengthTem)]
        plt.xticks(range(1, lengthTem + 1), dateDraw, rotation=60)
        plt.legend(loc='upper left', bbox_to_anchor=(0.01, 1.1), ncol=2, fancybox=True, shadow=True)
        winRatio = 'winRatio: ' + str(round(sum(resultsArray > 0) * 100 / len(resultsArray), 1)) + '%'
        sharpe = 'Sharpe：' + str(round(resultsArray.mean() / resultsArray.std(), 3))

        #锌交易情况
        if self.dateZn == False:
            data=w.wsi('zn.shf','close',startDayT+' 09:00:00',todayT+' 15:01:00',\
                   'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        else:
            datePast = self.dateZn.split(',')
            data = w.wsi('zn.shf', 'close', datePast[-1] + ' 09:00:00', todayT + ' 15:01:00', \
                         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        Points = data.Data[0]
        Dates = data.Times
        ResultT = -1
        DateT=-1
        L = len(Points)
        if L <5:
            return
        else:
            if L % 226 ==0:
                loop = L/226
            else:
                loop = L/226 +1

        for i in range(loop):
            if L<(i+1)*226:
                endi = L
            else:
                endi = (i+1)*226
            if endi-226 <0:
                starti = 0
            else:
                starti = (i)*226
            points=Points[starti:endi]
            lengthP = len(points)
            if lengthP > 5:
                resultT=-1
                dateT = datetime.date.strftime(Dates[i*226], '%Y%m%d')
                wd = Dates[i*226].weekday() + 1
                if wd == 1:
                    if lengthP >187:
                        resultT = points[172] / points[187] + points[70] / points[47] + points[27] / points[36] - 3
                    elif lengthP >172:
                        resultT = points[172] / points[-1] + points[70] / points[47] + points[27] / points[36] - 3
                    elif lengthP >70:
                        resultT = points[70] / points[47] + points[27] / points[36] - 2
                    elif lengthP >47:
                        resultT = points[-1] / points[47] + points[27] / points[36] - 2
                    elif lengthP >36:
                        resultT = points[27] / points[36] - 1
                    elif lengthP >27:
                        resultT = points[27] / points[-1] - 1
                elif wd == 2:
                    if lengthP >60:
                        resultT = points[9] / points[60] - 1
                    elif lengthP >9:
                        resultT = points[9] / points[-1] - 1
                elif wd == 3:
                    if lengthP >219:
                        resultT = points[219] / points[158] + points[99] / points[124] + points[39] / points[84] - 3
                    elif lengthP >158:
                        resultT = points[-1] / points[158] + points[99] / points[124] + points[39] / points[84] - 3
                    elif lengthP >124:
                        resultT = points[99] / points[124] + points[39] / points[84] - 2
                    elif lengthP >99:
                        resultT = points[99] / points[-1] + points[39] / points[84] - 2
                    elif lengthP >84:
                        resultT = points[39] / points[84] - 1
                    elif lengthP >39:
                        resultT = points[39] / points[-1] - 1
                elif wd == 4:
                    if lengthP >194:
                        resultT = points[183] / points[194] + points[135] / points[126] + points[72] / points[79] + points[70] / points[52] - 4
                    elif lengthP >183:
                        resultT = points[183] / points[-1] + points[135] / points[126] + points[72] / points[79] + points[70] / points[52] - 4
                    elif lengthP >135:
                        resultT = points[135] / points[126] + points[72] / points[79] + points[70] / points[52] - 3
                    elif lengthP >126:
                        resultT = points[-1] / points[126] + points[72] / points[79] + points[70] / points[52] - 3
                    elif lengthP >79:
                        resultT = points[72] / points[79] + points[70] / points[52] - 2
                    elif lengthP >72:
                        resultT = points[72] / points[-1] + points[70] / points[52] - 2
                    elif lengthP >70:
                        resultT = points[70] / points[52] - 1
                    elif lengthP >52:
                        resultT = points[-1] / points[52] - 1
                elif wd == 5:
                    if lengthP >224:
                        resultT = points[224] / points[210] + points[195] / points[200] + points[184] / points[173] + points[128] / points[85] - 4
                    elif lengthP >210:
                        resultT = points[-1] / points[210] + points[195] / points[200] + points[184] / points[173] + points[128] / points[85] - 4
                    elif lengthP >200:
                        resultT = points[195] / points[200] + points[184] / points[173] + points[128] / points[85] - 3
                    elif lengthP >195:
                        resultT = points[195] / points[-1] + points[184] / points[173] + points[128] / points[85] - 3
                    elif lengthP >184:
                        resultT = points[184] / points[173] + points[128] / points[85] - 2
                    elif lengthP >173:
                        resultT = points[-1] / points[173] + points[128] / points[85] - 2
                    elif lengthP >128:
                        resultT = points[128] / points[85] - 1
                    elif lengthP >85:
                        resultT = points[-1] / points[85] - 1

                if resultT != -1:
                    if ResultT == -1:
                        ResultT = [resultT]
                        DateT = [dateT]
                    else:
                        ResultT.append(resultT)
                        DateT.append(dateT)
        if ResultT == -1:
            return
        if self.resultsZnP == False:
            resultsDraw = ResultT
            dateDraw = DateT
        else:
            resultsDraw = map(eval,self.resultsZnP.split(','))[0:-1] + ResultT
            dateDraw = self.dateZn.split(',')[0:-1] + DateT
        self.dateZn =  ','.join(dateDraw)
        self.resultsZnP = ','.join(map(str,resultsDraw))

        lengthTem = len(resultsDraw)
        resultsArray=np.array(resultsDraw)
        resultsCum=resultsArray.cumsum()
        plt.plot(range(1, lengthTem + 1), resultsCum, label="锌测试")
        # xTicks = [dateUpdate.iloc[i].tolist()[0] for i in range(lengthTem)]
        plt.xticks(range(1, lengthTem + 1), dateDraw, rotation=60)
        plt.legend(loc='upper left', bbox_to_anchor=(0.01, 1.1), ncol=2, fancybox=True, shadow=True)
        plt.grid()
        winRatio = winRatio + '/' + str(round(sum(resultsArray>0)*100/len(resultsArray),1)) + '%;'
        sharpe = sharpe + '/' + str(round(resultsArray.mean()/resultsArray.std(),3))
        plt.figtext(0.41, 0.91, winRatio + sharpe, color='red', ha='left', fontsize=12, fontweight='bold',alpha=0.8, \
            bbox={'facecolor': 'gray', 'alpha': 0.5, 'pad': 0.3, 'edgecolor': 'None', 'boxstyle': 'round'},rotation="horizontal")  # transform=trans,
        picData = StringIO.StringIO()
        plt.savefig(picData)
        self.write({'pictureZn': base64.encodestring(picData.getvalue())})
        print 'Zn last results are as below: '
        print dateDraw[-1]
        print resultsDraw
        print resultsDraw[-1]

        # 新橡胶联合测试
        if self.dateRuNew == False:
            data=w.wsi('ru.shf','close',startDayT+' 09:00:00',todayT+' 15:01:00',\
                   'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        else:
            datePast = self.dateRuNew.split(',')
            data = w.wsi('ru.shf', 'close', datePast[-1] + ' 09:00:00', todayT + ' 15:01:00', \
                         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        Points = data.Data[0]
        Dates = data.Times
        ResultT = -1
        DateT=-1
        L = len(Points)
        if L <5:
            return
        else:
            if L % 226 ==0:
                loop = L/226
            else:
                loop = L/226 +1

        for i in range(loop):
            if L<(i+1)*226:
                endi = L
            else:
                endi = (i+1)*226
            if endi-226 <0:
                starti = 0
            else:
                starti = (i)*226
            points=Points[starti:endi]
            lengthP = len(points)
            if lengthP > 5:
                resultT=-1
                dateT = datetime.date.strftime(Dates[i*226], '%Y%m%d')
                wd = Dates[i*226].weekday() + 1
                if wd == 1:
                    if lengthP >200:
                        resultT = points[191] / points[200] + points[95] / points[85] + points[75] / points[85] - 3
                    elif lengthP >191:
                        resultT = points[191] / points[-1] + points[95] / points[85] + points[75] / points[85] - 3
                    elif lengthP >95:
                        resultT = points[95] / points[85] + points[75] / points[85] - 2
                    elif lengthP >85:
                        resultT = points[-1] / points[85] + points[75] / points[85] - 2
                    elif lengthP >75:
                        resultT = points[75] / points[-1] - 1
                elif wd == 2:
                    resultT = 0
                elif wd == 3:
                    resultT = 0
                elif wd == 4:
                    if lengthP >200:
                        resultT = points[188] / points[200] + points[150] / points[156] + points[15] / points[30] - 3
                    elif lengthP >188:
                        resultT = points[188] / points[-1] + points[150] / points[156] + points[15] / points[30] - 3
                    elif lengthP >156:
                        resultT = points[150] / points[156] + points[15] / points[30] - 2
                    elif lengthP >150:
                        resultT = points[150] / points[-1] + points[15] / points[30] - 2
                    elif lengthP >30:
                        resultT = points[15] / points[30] - 1
                    elif lengthP >15:
                        resultT = points[15] / points[-1] - 1
                elif wd == 5:
                    if lengthP >66:
                        resultT = points[50] / points[66] - 1
                    elif lengthP >50:
                        resultT = points[50] / points[-1] - 1

                if resultT != -1:
                    if ResultT == -1:
                        ResultT = [resultT]
                        DateT = [dateT]
                    else:
                        ResultT.append(resultT)
                        DateT.append(dateT)
        if ResultT == -1:
            return
        if self.resultsRuPNew == False:
            resultsDraw = ResultT
            dateDraw = DateT
        else:
            resultsDraw = map(eval,self.resultsRuPNew.split(','))[0:-1] + ResultT
            dateDraw = self.dateRuNew.split(',')[0:-1] + DateT
        self.dateRuNew =  ','.join(dateDraw)
        self.resultsRuPNew = ','.join(map(str,resultsDraw))

        plt.figure(figsize=(15, 6))
        lengthTem = len(resultsDraw)
        resultsArray = np.array(resultsDraw)
        resultsCum = resultsArray.cumsum()
        plt.plot(range(1, lengthTem + 1), resultsCum, label="新橡胶测试")
        # xTicks = [dateUpdate.iloc[i].tolist()[0] for i in range(lengthTem)]
        plt.xticks(range(1, lengthTem + 1), dateDraw, rotation=60)
        plt.legend(loc='upper left', bbox_to_anchor=(0.01, 1.1), ncol=2, fancybox=True, shadow=True)
        winRatio = 'winRatio: ' + str(round(sum(resultsArray > 0) * 100 / len(resultsArray), 1)) + '%'
        sharpe = 'Sharpe：' + str(round(resultsArray.mean() / resultsArray.std(), 3))

        #橡胶测试
        if self.dateRu == False:
            data=w.wsi('ru.shf','close',startDayT+' 09:00:00',todayT+' 15:01:00',\
                   'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        else:
            datePast = self.dateRu.split(',')
            data = w.wsi('ru.shf', 'close', datePast[-1] + ' 09:00:00', todayT + ' 15:01:00', \
                         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        Points = data.Data[0]
        Dates = data.Times
        ResultT = -1
        DateT=-1
        L = len(Points)
        if L <5:
            return
        else:
            if L % 226 ==0:
                loop = L/226
            else:
                loop = L/226 +1

        for i in range(loop):
            if L<(i+1)*226:
                endi = L
            else:
                endi = (i+1)*226
            if endi-226 <0:
                starti = 0
            else:
                starti = (i)*226
            points=Points[starti:endi]
            lengthP = len(points)
            if lengthP > 5:
                resultT=-1
                dateT = datetime.date.strftime(Dates[i*226], '%Y%m%d')
                wd = Dates[i*226].weekday() + 1
                if wd == 1:
                    if lengthP >170:
                        resultT = points[158] / points[170] + points[150] / points[138] + points[115] / points[108] + points[61] / points[69] - 4
                    elif lengthP >158:
                        resultT = points[158] / points[-1] + points[150] / points[138] + points[115] / points[108] + points[61] / points[69] - 4
                    elif lengthP >150:
                        resultT = points[150] / points[138] + points[115] / points[108] + points[61] / points[69] - 3
                    elif lengthP >138:
                        resultT = points[-1] / points[138] + points[115] / points[108] + points[61] / points[69] - 3
                    elif lengthP >115:
                        resultT = points[115] / points[108] + points[61] / points[69] - 2
                    elif lengthP >108:
                        resultT = points[-1] / points[108] + points[61] / points[69] - 2
                    elif lengthP >69:
                        resultT = points[61] / points[69] - 1
                    elif lengthP >61:
                        resultT = points[61] / points[-1] - 1
                elif wd == 2:
                    if lengthP >125:
                        resultT = points[90] / points[125] + points[74] / points[63] + points[22] / points[60] - 3
                    elif lengthP >90:
                        resultT = points[90] / points[-1] + points[74] / points[63] + points[22] / points[60] - 3
                    elif lengthP >74:
                        resultT = points[74] / points[63] + points[22] / points[60] - 2
                    elif lengthP >63:
                        resultT = points[-1] / points[63] + points[22] / points[60] - 2
                    elif lengthP >60:
                        resultT = points[22] / points[60] - 1
                    elif lengthP >22:
                        resultT = points[22] / points[-1]  - 1
                elif wd == 3:
                    if lengthP >194:
                        resultT = points[194] / points[181] + points[100] / points[111] + points[100] / points[95] + points[47] / points[62] + points[24] / points[33] - 5
                    elif lengthP >181:
                        resultT = points[-1] / points[181] + points[100] / points[111] + points[100] / points[95] + points[47] / points[62] + points[24] / points[33] - 5
                    elif lengthP >111:
                        resultT = points[100] / points[111] + points[100] / points[95] + points[47] / points[62] + points[24] / points[33] - 4
                    elif lengthP >100:
                        resultT = points[100] / points[-1] + points[100] / points[95] + points[47] / points[62] + points[24] / points[33] - 4
                    elif lengthP >95:
                        resultT =  points[-1] / points[95] + points[47] / points[62] + points[24] / points[33] - 3
                    elif lengthP >62:
                        resultT = points[47] / points[62] + points[24] / points[33] - 2
                    elif lengthP >47:
                        resultT = points[47] / points[-1] + points[24] / points[33] - 2
                    elif lengthP >33:
                        resultT = points[24] / points[33] - 1
                    elif lengthP >24:
                        resultT = points[24] / points[-1] - 1
                elif wd == 4:
                    if lengthP >79:
                        resultT = points[71] / points[79] + points[24] / points[32] + points[14] / points[9] - 3
                    elif lengthP >71:
                        resultT = points[71] / points[-1] + points[24] / points[32] + points[14] / points[9] - 3
                    elif lengthP >32:
                        resultT = points[24] / points[32] + points[14] / points[9] - 2
                    elif lengthP >24:
                        resultT = points[24] / points[-1] + points[14] / points[9] - 2
                    elif lengthP >14:
                        resultT = points[14] / points[9] - 1
                    elif lengthP >9:
                        resultT = points[-1] / points[9] - 1
                elif wd == 5:
                    if lengthP >80:
                        resultT = points[74] / points[80] - 1
                    elif lengthP >74:
                        resultT = points[74] / points[-1] - 1

                if resultT != -1:
                    if ResultT == -1:
                        ResultT = [resultT]
                        DateT = [dateT]
                    else:
                        ResultT.append(resultT)
                        DateT.append(dateT)
        if ResultT == -1:
            return
        if self.resultsRuP == False:
            resultsDraw = ResultT
            dateDraw = DateT
        else:
            resultsDraw = map(eval,self.resultsRuP.split(','))[0:-1] + ResultT
            dateDraw = self.dateRu.split(',')[0:-1] + DateT
        self.dateRu =  ','.join(dateDraw)
        self.resultsRuP = ','.join(map(str,resultsDraw))

        lengthTem = len(resultsDraw)
        resultsArray=np.array(resultsDraw)
        resultsCum=resultsArray.cumsum()
        plt.plot(range(1, lengthTem + 1), resultsCum, label="橡胶测试")
        # xTicks = [dateUpdate.iloc[i].tolist()[0] for i in range(lengthTem)]
        plt.xticks(range(1, lengthTem + 1), dateDraw, rotation=60)
        plt.legend(loc='upper left', bbox_to_anchor=(0.01, 1.1), ncol=2, fancybox=True, shadow=True)
        plt.grid()
        winRatio = winRatio + '/' + str(round(sum(resultsArray > 0) * 100 / len(resultsArray), 1)) + '%;'
        sharpe = sharpe + '/' + str(round(resultsArray.mean() / resultsArray.std(), 3))
        plt.figtext(0.41, 0.91, winRatio + sharpe, color='red', ha='left', fontsize=12, fontweight='bold', alpha=0.8, \
            bbox={'facecolor': 'gray', 'alpha': 0.5, 'pad': 0.3, 'edgecolor': 'None', 'boxstyle': 'round'},rotation="horizontal")  # transform=trans,
        picData = StringIO.StringIO()
        plt.savefig(picData)
        self.write({'pictureRu': base64.encodestring(picData.getvalue())})
        print 'Ru last results are as below: '
        print dateDraw[-1]
        print resultsDraw
        print resultsDraw[-1]

        if self.dateWh == False:
            data=w.wsi('wh.czc','close',startDayT+' 09:00:00',todayT+' 15:01:00',\
                   'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        else:
            datePast = self.dateWh.split(',')
            data = w.wsi('wh.czc', 'close', datePast[-1] + ' 09:00:00', todayT + ' 15:01:00', \
                         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        Points = data.Data[0]
        Dates = data.Times
        ResultT = -1
        DateT=-1
        L = len(Points)
        if L <5:
            return
        else:
            if L % 226 ==0:
                loop = L/226
            else:
                loop = L/226 +1

        for i in range(loop):
            if L<(i+1)*226:
                endi = L
            else:
                endi = (i+1)*226
            if endi-226 <0:
                starti = 0
            else:
                starti = (i)*226
            points=Points[starti:endi]
            lengthP = len(points)
            if lengthP > 5:
                resultT=-1
                dateT = datetime.date.strftime(Dates[i*226], '%Y%m%d')
                wd = Dates[i*226].weekday() + 1
                if wd == 1:
                    if lengthP >199:
                        resultT = points[199] / points[186] + points[143] / points[148] + points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 5
                    elif lengthP >186:
                        resultT = points[-1] / points[186] + points[143] / points[148] + points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 5
                    elif lengthP >148:
                        resultT = points[143] / points[148] + points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 4
                    elif lengthP >143:
                        resultT = points[143] / points[-1] + points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 4
                    elif lengthP >108:
                        resultT =  points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 3
                    elif lengthP >99:
                        resultT = points[-1] / points[99] + points[24] / points[19] + points[5] / points[10] - 3
                    elif lengthP >24:
                        resultT = points[24] / points[19] + points[5] / points[10] - 2
                    elif lengthP >19:
                        resultT = points[-1] / points[19] + points[5] / points[10] - 2
                    elif lengthP >10:
                        resultT = points[5] / points[10] - 1
                    elif lengthP >5:
                        resultT = points[5] / points[-1] - 1
                elif wd == 2:
                    if lengthP >144:
                        resultT = points[131] / points[144] + points[111] / points[118] + points[20] / points[8] + points[1] / points[8] - 4
                    elif lengthP >131:
                        resultT = points[131] / points[-1] + points[111] / points[118] + points[20] / points[8] + points[1] / points[8] - 4
                    elif lengthP >118:
                        resultT = points[111] / points[118] + points[20] / points[8] + points[1] / points[8] - 3
                    elif lengthP >111:
                        resultT = points[111] / points[-1] + points[20] / points[8] + points[1] / points[8] - 3
                    elif lengthP >20:
                        resultT = points[20] / points[8] + points[1] / points[8] - 2
                    elif lengthP >8:
                        resultT = points[-1] / points[8] + points[1] / points[8] - 2
                    elif lengthP >1:
                        resultT = points[1] / points[-1] - 1
                elif wd == 3:
                    if lengthP >219:
                        resultT = points[219] / points[211] + points[186] / points[153] + points[64] / points[71] - 3
                    elif lengthP >211:
                        resultT = points[-1] / points[211] + points[186] / points[153] + points[64] / points[71] - 3
                    elif lengthP >186:
                        resultT = points[186] / points[153] + points[64] / points[71] - 2
                    elif lengthP >153:
                        resultT = points[-1] / points[153] + points[64] / points[71] - 2
                    elif lengthP >71:
                        resultT = points[64] / points[71] - 1
                    elif lengthP >64:
                        resultT = points[64] / points[-1] - 1
                elif wd == 4:
                    if lengthP >223:
                        resultT = points[223] / points[216] + points[195] / points[202] + points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 6
                    elif lengthP >216:
                        resultT = points[-1] / points[216] + points[195] / points[202] + points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 6
                    elif lengthP >202:
                        resultT = points[195] / points[202] + points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 5
                    elif lengthP >195:
                        resultT = points[195] / points[-1] + points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 5
                    elif lengthP >172:
                        resultT = points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 4
                    elif lengthP >163:
                        resultT = points[163] / points[-1] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 4
                    elif lengthP >128:
                        resultT =  points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 3
                    elif lengthP >117:
                        resultT = points[117] / points[-1] + points[117] / points[92] + points[12] / points[16] - 3
                    elif lengthP >92:
                        resultT = points[-1] / points[92] + points[12] / points[16] - 2
                    elif lengthP >16:
                        resultT = points[12] / points[16] - 1
                    elif lengthP >12:
                        resultT = points[12] / points[-1] - 1
                elif wd == 5:
                    if lengthP >212:
                        resultT = points[201] / points[212] + points[152] / points[164] + points[134] / points[142] - 3
                    elif lengthP >201:
                        resultT = points[201] / points[-1] + points[152] / points[164] + points[134] / points[142] - 3
                    elif lengthP >164:
                        resultT = points[152] / points[164] + points[134] / points[142] - 2
                    elif lengthP >152:
                        resultT = points[152] / points[-1] + points[134] / points[142] - 2
                    elif lengthP >142:
                        resultT = points[134] / points[142] - 1
                    elif lengthP >134:
                        resultT = points[134] / points[-1] - 1

                if resultT != -1:
                    if ResultT == -1:
                        ResultT = [resultT]
                        DateT = [dateT]
                    else:
                        ResultT.append(resultT)
                        DateT.append(dateT)
        if ResultT == -1:
            return
        if self.resultsWhP == False:
            resultsDraw = ResultT
            dateDraw = DateT
        else:
            resultsDraw = map(eval,self.resultsWhP.split(','))[0:-1] + ResultT
            dateDraw = self.dateWh.split(',')[0:-1] + DateT
        self.dateWh =  ','.join(dateDraw)
        self.resultsWhP = ','.join(map(str,resultsDraw))

        plt.figure(figsize=(15, 6))
        lengthTem = len(resultsDraw)
        resultsArray=np.array(resultsDraw)
        resultsCum=resultsArray.cumsum()
        plt.plot(range(1, lengthTem + 1), resultsCum, label="策略实时测试")
        # xTicks = [dateUpdate.iloc[i].tolist()[0] for i in range(lengthTem)]
        plt.xticks(range(1, lengthTem + 1), dateDraw, rotation=60)
        plt.legend(loc='upper left', bbox_to_anchor=(0.01, 1.1), ncol=2, fancybox=True, shadow=True)
        plt.grid()
        winRatio = 'winRatio: ' + str(round(sum(resultsArray > 0) * 100 / len(resultsArray), 1)) + '%;'
        sharpe = 'Sharpe：' + str(round(resultsArray.mean() / resultsArray.std(), 3))
        plt.figtext(0.41, 0.91, winRatio + sharpe, color='red', ha='left', fontsize=12, fontweight='bold', alpha=0.8, \
            bbox={'facecolor': 'gray', 'alpha': 0.5, 'pad': 0.3, 'edgecolor': 'None', 'boxstyle': 'round'},rotation="horizontal")  # transform=trans,
        picData = StringIO.StringIO()
        plt.savefig(picData)
        self.write({'pictureWh': base64.encodestring(picData.getvalue())})
        print 'Wheet last results are as below: '
        print dateDraw[-1]
        print resultsDraw
        print resultsDraw[-1]

        if self.dateM == False:
            data=w.wsi('m.dce','close',startDayT+' 09:00:00',todayT+' 15:01:00',\
                   'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        else:
            datePast = self.dateM.split(',')
            data = w.wsi('m.dce', 'close', datePast[-1] + ' 09:00:00', todayT + ' 15:01:00', \
                         'periodstart=09:00:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
        Points = data.Data[0]
        Dates = data.Times
        ResultT = -1
        DateT=-1
        L = len(Points)
        if L <5:
            return
        else:
            if L % 226 ==0:
                loop = L/226
            else:
                loop = L/226 +1

        for i in range(loop):
            if L<(i+1)*226:
                endi = L
            else:
                endi = (i+1)*226
            if endi-226 <0:
                starti = 0
            else:
                starti = (i)*226
            points=Points[starti:endi]
            lengthP = len(points)
            if lengthP > 5:
                resultT=-1
                dateT = datetime.date.strftime(Dates[i*226], '%Y%m%d')
                wd = Dates[i*226].weekday() + 1
                if wd == 1:
                    if lengthP >199:
                        resultT = points[199] / points[186] + points[143] / points[148] + points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 5
                    elif lengthP >186:
                        resultT = points[-1] / points[186] + points[143] / points[148] + points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 5
                    elif lengthP >148:
                        resultT = points[143] / points[148] + points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 4
                    elif lengthP >143:
                        resultT = points[143] / points[-1] + points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 4
                    elif lengthP >108:
                        resultT =  points[108] / points[99] + points[24] / points[19] + points[5] / points[10] - 3
                    elif lengthP >99:
                        resultT = points[-1] / points[99] + points[24] / points[19] + points[5] / points[10] - 3
                    elif lengthP >24:
                        resultT = points[24] / points[19] + points[5] / points[10] - 2
                    elif lengthP >19:
                        resultT = points[-1] / points[19] + points[5] / points[10] - 2
                    elif lengthP >10:
                        resultT = points[5] / points[10] - 1
                    elif lengthP >5:
                        resultT = points[5] / points[-1] - 1
                elif wd == 2:
                    if lengthP >144:
                        resultT = points[131] / points[144] + points[111] / points[118] + points[20] / points[8] + points[1] / points[8] - 4
                    elif lengthP >131:
                        resultT = points[131] / points[-1] + points[111] / points[118] + points[20] / points[8] + points[1] / points[8] - 4
                    elif lengthP >118:
                        resultT = points[111] / points[118] + points[20] / points[8] + points[1] / points[8] - 3
                    elif lengthP >111:
                        resultT = points[111] / points[-1] + points[20] / points[8] + points[1] / points[8] - 3
                    elif lengthP >20:
                        resultT = points[20] / points[8] + points[1] / points[8] - 2
                    elif lengthP >8:
                        resultT = points[-1] / points[8] + points[1] / points[8] - 2
                    elif lengthP >1:
                        resultT = points[1] / points[-1] - 1
                elif wd == 3:
                    if lengthP >219:
                        resultT = points[219] / points[211] + points[186] / points[153] + points[64] / points[71] - 3
                    elif lengthP >211:
                        resultT = points[-1] / points[211] + points[186] / points[153] + points[64] / points[71] - 3
                    elif lengthP >186:
                        resultT = points[186] / points[153] + points[64] / points[71] - 2
                    elif lengthP >153:
                        resultT = points[-1] / points[153] + points[64] / points[71] - 2
                    elif lengthP >71:
                        resultT = points[64] / points[71] - 1
                    elif lengthP >64:
                        resultT = points[64] / points[-1] - 1
                elif wd == 4:
                    if lengthP >223:
                        resultT = points[223] / points[216] + points[195] / points[202] + points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 6
                    elif lengthP >216:
                        resultT = points[-1] / points[216] + points[195] / points[202] + points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 6
                    elif lengthP >202:
                        resultT = points[195] / points[202] + points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 5
                    elif lengthP >195:
                        resultT = points[195] / points[-1] + points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 5
                    elif lengthP >172:
                        resultT = points[163] / points[172] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 4
                    elif lengthP >163:
                        resultT = points[163] / points[-1] + points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 4
                    elif lengthP >128:
                        resultT =  points[117] / points[128] + points[117] / points[92] + points[12] / points[16] - 3
                    elif lengthP >117:
                        resultT = points[117] / points[-1] + points[117] / points[92] + points[12] / points[16] - 3
                    elif lengthP >92:
                        resultT = points[-1] / points[92] + points[12] / points[16] - 2
                    elif lengthP >16:
                        resultT = points[12] / points[16] - 1
                    elif lengthP >12:
                        resultT = points[12] / points[-1] - 1
                elif wd == 5:
                    if lengthP >212:
                        resultT = points[201] / points[212] + points[152] / points[164] + points[134] / points[142] - 3
                    elif lengthP >201:
                        resultT = points[201] / points[-1] + points[152] / points[164] + points[134] / points[142] - 3
                    elif lengthP >164:
                        resultT = points[152] / points[164] + points[134] / points[142] - 2
                    elif lengthP >152:
                        resultT = points[152] / points[-1] + points[134] / points[142] - 2
                    elif lengthP >142:
                        resultT = points[134] / points[142] - 1
                    elif lengthP >134:
                        resultT = points[134] / points[-1] - 1

                if resultT != -1:
                    if ResultT == -1:
                        ResultT = [resultT]
                        DateT = [dateT]
                    else:
                        ResultT.append(resultT)
                        DateT.append(dateT)
        if ResultT == -1:
            return
        if self.resultsMP == False:
            resultsDraw = ResultT
            dateDraw = DateT
        else:
            resultsDraw = map(eval,self.resultsMP.split(','))[0:-1] + ResultT
            dateDraw = self.dateM.split(',')[0:-1] + DateT
        self.dateM =  ','.join(dateDraw)
        self.resultsMP = ','.join(map(str,resultsDraw))

        plt.figure(figsize=(15, 6))
        lengthTem = len(resultsDraw)
        resultsArray=np.array(resultsDraw)
        resultsCum=resultsArray.cumsum()
        plt.plot(range(1, lengthTem + 1), resultsCum, label="策略实时测试")
        # xTicks = [dateUpdate.iloc[i].tolist()[0] for i in range(lengthTem)]
        plt.xticks(range(1, lengthTem + 1), dateDraw, rotation=60)
        plt.legend(loc='upper left', bbox_to_anchor=(0.01, 1.1), ncol=2, fancybox=True, shadow=True)
        plt.grid()
        winRatio = 'winRatio: ' + str(round(sum(resultsArray > 0) * 100 / len(resultsArray), 1)) + '%;'
        sharpe = 'Sharpe：' + str(round(resultsArray.mean() / resultsArray.std(), 3))
        plt.figtext(0.41, 0.91, winRatio + sharpe, color='red', ha='left', fontsize=12, fontweight='bold', alpha=0.8, \
            bbox={'facecolor': 'gray', 'alpha': 0.5, 'pad': 0.3, 'edgecolor': 'None', 'boxstyle': 'round'},rotation="horizontal")  # transform=trans,
        picData = StringIO.StringIO()
        plt.savefig(picData)
        self.write({'pictureM': base64.encodestring(picData.getvalue())})
        print 'Dou Po last results are as below: '
        print dateDraw[-1]
        print resultsDraw
        print resultsDraw[-1]



























        #endDate=datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
        #days=endDate-datetime.datetime.strptime(self.startDate, "%Y-%m-%d").date()
        #daysL=days.days
        #startM=datetime.datetime.strptime(self.startDate,'%Y-%m-%d').month-1
        #stock=stocks.loc[startM,:].tolist()
        #w.start()
        #close=w.wsd(stock,'close',self.startDate,endDate)

        #close=pd.DataFrame(close.Data)
        #trading=0
        #test = w.wsd('000001.SH', 'high')
        #if not isinstance(test.Data[0][0],float):
            #trading=1
            #closeLatest=w.wsq(stock, "rt_last")
        #for i in range(close.shape[0]+trading):









'''
        indMonth=datetime.datetime.now().month-1
        if self.notes<0 or self.notes!=indMonth:
            self.notes=indMonth
            stock=stocksM.loc[indMonth,:].tolist()



        w.start()
        plt.figure(figsize=(18, 6))
        dataTem=w.wsd('000001.SH','close','ED-50TD','2017-03-13')
        yTest=dataTem.Data[0]
        test = w.wsd('000001.SH','high')
        if not isinstance(test.Data[0][0],float):
            plt.plot(yTest)
            picData = StringIO.StringIO()
            plt.savefig(picData)
            self.write({self.picture: base64.encodestring(picData.getvalue())})
        else:
            dataTem = w.wsq("000001.SH", "rt_last")
            yTest.append(dataTem.Data[0][0])
            plt.plot(yTest)
            picData = StringIO.StringIO()
            plt.savefig(picData)
            self.write({'picture': base64.encodestring(picData.getvalue())})
'''








'''
        w.start()
        def funCycle(indata):
            data=np.random.rand(1)
            print data
            print str(data)
        w.wsq("000001.SH,000001.SZ", "rt_last", func=funCycle)
'''

'''
fig = plt.figure()
ax=fig.add_axes([0.1,0.1,0.9,0.9])
dataTem=ts.get_k_data(self.stock,start='2017-01-01',index=self.indexButton)
fig,ax=plt.subplots()
mpf.candlestick2_ohlc(ax,dataTem['open'],dataTem['high'],dataTem['low'],dataTem['close'],width=0.6)
plt.grid(True)
ax.autoscale_view()
'''


'''
@api.multi
    def figplot(self,cr):
      fig=plt.figure()
      ax=fig.add_axes([0.1,0.1,0.9,0.9])
      dataTem=ts.get_k_data('600000',start='2017-01-01')
      fig,ax=plt.subplots()
      mpf.candlestick2_ohlc(ax,dataTem['open'],dataTem['high'],dataTem['low'],dataTem['close'],width=0.6)
      plt.grid(True)
      ax.autoscale_view()
      tem='D:\%s.png' % cr['uid']
      plt.savefig(tem)
      pic_data=open(tem,'rb').read()
      self.write({'picture':base64.encodestring(pic_data)})
      os.remove(tem)

'''



'''
 @api.multi
    def plotfig(self,cr):
      file_like=io.BytesIO(base64.b64decode(self.datafile))
      table=pandas.read_excel(file_like,header=None)#header=None
      col_names=table.iloc[0,:]
      fig=plt.figure()
      ax=fig.add_axes([0.1,0.1,0.65,0.85])
      plot_yy=False
      L=[]
      L_names=[]
      index_color=-1
      last_color=''
      colors=['r','g','b','y','c','m','k','w']
      for i in np.arange(1,len(col_names),2):
        if index_color==8:
          raise exceptions.Warning(u'最多同时画8种线，否则颜色难辨！')
          break
        if not plot_yy:
          if type(table.iloc[2,i])==int or type(table.iloc[2,i])==float:
            x_tem=table.iloc[1:,i]
            y_tem=table.iloc[1:,i+1]
            if last_color!=col_names[i]:
              index_color+=1
              last_color=col_names[i]
            tem,=ax.plot(x_tem,y_tem,linewidth=2,color=colors[index_color])
            L.append(tem)
            L_names.append(col_names[i])
            ax.plot(x_tem,y_tem,'k*')
          else:
            ax.grid(True)
            #ax.spines['right'].set_color('none')
            #ax.spines['top'].set_color('none')
            #ax.spines['bottom'].set_position(('data',0))
            #ax.spines['left'].set_position(('data',0))
            plt.title(col_names[0],fontweight='bold')
            plt.xlabel(table.iloc[1,0])
            plt.ylabel(table.iloc[2,0])
            plot_yy=True
            axc=ax.twinx()
            plt.ylabel(table.iloc[2,i])
        if plot_yy:
          if i+1<len(col_names):
            x_tem=table.iloc[1:,i+1]
            y_tem=table.iloc[1:,i+2]
            if last_color!=col_names[i]:
              index_color+=1
              last_color=col_names[i+1]
            tem,=axc.plot(x_tem,y_tem,linewidth=2,color=colors[index_color])
            L.append(tem)
            L_names.append(col_names[i+1])
            axc.plot(x_tem,y_tem,'k*')
      fig.legend(L,L_names,loc='right',ncol=1,shadow=True,title=u'图例')#,bbox_to_anchor=[1.0, 0.5]
      tem='/tmp/%s.png' % cr['uid']
      plt.savefig(tem)
      pic_data=open(tem,'rb').read()
      self.write({'picture':base64.encodestring(pic_data)})
      os.remove(tem)
'''


