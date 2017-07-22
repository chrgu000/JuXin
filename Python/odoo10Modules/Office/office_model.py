# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions
import base64,io,pandas,os #,StringIO,openpyxl,xlrd,matplotlib
import matplotlib.pyplot as plt
import numpy as np
from odoo.exceptions import ValidationError
#matplotlib.use('Agg')

import sys # kick  ascii code errors
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

from pylab import *  # for Chinese charactors
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

class PunchTask(models.Model):
    _name = 'punch.task'
    _description = 'Punch task'
    name=fields.Char()
    datafile = fields.Binary(u'选择考勤Excel表', required=True)
    duty_on = fields.Text(u'8:30前没打卡')
    duty_off = fields.Text(u'17:00后没打卡')

    @api.multi
    def select_odd(self, cr):
        self.name = self.env.user.name + '修改于：' + fields.Date.today()
        file_like = io.BytesIO(base64.b64decode(self.datafile))
        # datax=pandas.read_excel(file_like)
        table = pandas.ExcelFile(file_like)
        col_name = table.parse(0).icol(1).real[1:]
        col_datetime = table.parse(0).icol(3)[1:]

        col_date = []
        col_time = []
        for c in col_datetime:
            col_date.append(c[:10])
            col_time.append(c[11:])
        date_unique = list(set(col_date))

        date_unique_copy = date_unique  # delete the possible holiday which workers are less than 4 presons;
        for date_i in date_unique_copy:
            index_tmp = [i for i, key in enumerate(col_date) if key == date_i]
            date_name = [col_name[j] for j in index_tmp]
            if len(set(date_name)) <= 3:
                date_unique.remove(date_i)

        name_unique = list(set(col_name))
        duty_on = []
        duty_off = []
        for i in range(len(col_time)):
            if col_time[i] < '08:31:00':
                duty_on.append(i)
            elif col_time[i] > '17:00:00':
                duty_off.append(i)

        self.duty_on = self.get_string(name_unique, date_unique, col_name, col_date, duty_on)
        self.duty_off = self.get_string(name_unique, date_unique, col_name, col_date, duty_off)

    def get_string(self, name_unique, date_unique, col_name, col_date, duty):
        duty_on_record = []  # 创建存储每个人的上班打卡的所有日期;duty_on_record记录每个人上班打卡正常的所有日期;duty_on_record_copy存储每个人(第一个元素是姓名)打没打卡的情况;
        duty_on_record_copy = []
        for i in range(len(name_unique)):
            duty_on_record.append([])
            duty_on_record_copy.append([])
            duty_on_record_copy[i].append(name_unique[i])

        for i in duty:
            for index in range(len(name_unique)):
                if col_name[i] == name_unique[index]:
                    duty_on_record[index].append(col_date[i])
                    break

        duty_on_output = []
        for i in range(len(duty_on_record)):
            for date in date_unique:
                if date not in duty_on_record[i]:
                    # duty_on_output.append(','.join([name_unique[i],date]))
                    duty_on_record_copy[i].append(date)
        tmp = []
        for i in range(len(duty_on_record_copy)):
            if len(duty_on_record_copy[i]) > 1:
                tmp.append(' '.join(duty_on_record_copy[i]))

        return '\n'.join(tmp)  # '\n'.join(duty_on_output)

class PlotPointsTask(models.Model):
    _name = 'plotpoints.task'
    _description = 'Plot Points task'
    name=fields.Char()
    datafile = fields.Binary(u'选择xlsx数据表', required=True)
    picture = fields.Binary(u'图像')

    @api.multi
    def plotfig(self, cr):
        self.name = self.env.user.name + '修改于：' + fields.Date.today()
        file_like = io.BytesIO(base64.b64decode(self.datafile))
        table = pandas.read_excel(file_like, header=None)  # header=None
        col_names = table.iloc[0, :]
        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.1, 0.65, 0.85])
        plot_yy = False
        L = []
        L_names = []
        index_color = -1
        last_color = ''
        colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'w']
        for i in np.arange(1, len(col_names), 2):
            if index_color == 8:
                raise exceptions.Warning(u'最多同时画8种线，否则颜色难辨！')
                break
            if not plot_yy:
                if type(table.iloc[2, i]) == int or type(table.iloc[2, i]) == float:
                    x_tem = table.iloc[1:, i]
                    y_tem = table.iloc[1:, i + 1]
                    if last_color != col_names[i]:
                        index_color += 1
                        last_color = col_names[i]
                    tem, = ax.plot(x_tem, y_tem, linewidth=2, color=colors[index_color])
                    L.append(tem)
                    L_names.append(col_names[i])
                    ax.plot(x_tem, y_tem, 'k*')
                else:
                    ax.grid(True)
                    # ax.spines['right'].set_color('none')
                    # ax.spines['top'].set_color('none')
                    # ax.spines['bottom'].set_position(('data',0))
                    # ax.spines['left'].set_position(('data',0))
                    plt.title(col_names[0], fontweight='bold')
                    plt.xlabel(table.iloc[1, 0])
                    plt.ylabel(table.iloc[2, 0])
                    plot_yy = True
                    axc = ax.twinx()
                    plt.ylabel(table.iloc[2, i])
            if plot_yy:
                if i + 1 < len(col_names):
                    x_tem = table.iloc[1:, i + 1]
                    y_tem = table.iloc[1:, i + 2]
                    if last_color != col_names[i]:
                        index_color += 1
                        last_color = col_names[i + 1]
                    tem, = axc.plot(x_tem, y_tem, linewidth=2, color=colors[index_color])
                    L.append(tem)
                    L_names.append(col_names[i + 1])
                    axc.plot(x_tem, y_tem, 'k*')
        fig.legend(L, L_names, loc='right', ncol=1, shadow=True, title=u'图例')  # ,bbox_to_anchor=[1.0, 0.5]
        tem = 'd:\%s.png' % cr['uid']
        plt.savefig(tem)
        pic_data = open(tem, 'rb').read()
        self.write({'picture': base64.encodestring(pic_data)})
        os.remove(tem)

