# -*- coding: utf-8 -*-
from openerp import models, fields,api
from openerp.exceptions import ValidationError
#from datetime import date, timedelta


class DetectionTask(models.Model):
    _name = 'detection.task'
    _description = 'Detection task'
    #_inherit = ['mail.thread']

    NO = fields.Char('编号')
    Lot = fields.Char('批号')
    #Writer_name=fields.Char(related="write_uid.name", "修改者") #仅仅显示修改者的名字字符;
    Pro=fields.Float('蛋白含量（%）',(4,2))
    Pro_copy=fields.Float('蛋白含量（%）',compute='_for_readonly')
    pro=fields.Boolean('蛋白含量(%)')
    H2O=fields.Float('水分（%）',(4,2))
    H2O_copy=fields.Float('水分（%）',compute='_for_readonly')
    h2o=fields.Boolean('水分(%)')
    CPC=fields.Float('CPC（%）',(4,2))
    CPC_copy=fields.Float('CPC（%）',compute='_for_readonly')
    cpc=fields.Boolean('CPC(%)')
    Metal=fields.Float('重金属（%）',(4,2))
    Metal_copy=fields.Float('重金属（%）',compute='_for_readonly')
    metal=fields.Boolean('重金属(%)')
    Active=fields.Boolean('确认收样',default=False)
    #Applicant=fields.Many2one('res.users','请验人:')#, compute='for_Applicant'
    Receiver=fields.Many2one('res.users', string='收样人:')#,compute='_for_Receiver'
    Date_receive=fields.Datetime('收样日期:')

    @api.multi
    def write(self, vals): # can accept "readonly" in xml file;
        if 'Active' in vals:
            vals.update({'Receiver': self._uid,'Date_receive':fields.Datetime.now()})
        return super(DetectionTask, self).write(vals)

    @api.multi
    def _for_readonly(self):
        if self.Pro:
            self.Pro_copy=self.Pro
        if self.H2O:
            self.H2O_copy=self.H2O
        if self.CPC:
            self.CPC_copy=self.CPC
        if self.Metal:
            self.Metal_copy=self.Metal

    @api.constrains('Pro','H2O','CPC','Metal')
    def _check_Float(self):
        if (self.Pro<0 or self.Pro>100) or \
           (self.H2O<0 or self.H2O>100) or \
           (self.CPC<0 or self.CPC>100) or \
           (self.Metal<0 or self.Metal>100):
           raise ValidationError("输入的数字必须在0~100之间!")

'''
class MyClass(...):

    def create(cr, uid, vals, context=None):
        # Your logic goes here or call your method
        res_id = super(MyClass, self).create(cr, uid, vals, context=context)
        # Your logic goes here or call your method
        return res_id

    def write(cr, uid, ids, vals, context=None):
        # Your logic goes here or call your method
        super(MyClass, self).write(cr, uid, ids, vals, context=context)
        # Your logic goes here or call your method
        return True
#Create method will be called when you are creating a new record.If you are updating any existing record, write method will be called.

'''

'''
    @api.onchange("Active") # can't accept "readonly" in xml file;
    def for_Receiver(self):
        if self.Active:
            self.Receiver=self.env.uid
            self.Date_receive=fields.Datetime.now()#.strftime(DATE_FMT)#date.today()#fields.Date.today()
'''

'''
    @api.onchange("NO","Lot")
    def for_Applicant(self):
        if self.NO:
            self.Applicant=self.env.uid
'''


'''
    @api.depends('Active')
    def _for_Receiver(self):
        self.Receiver=self.env.uid
        return {
            'warning':{
                'title':"确认收样",
                'message':"收样成功!",
            }
        }
'''   

    




