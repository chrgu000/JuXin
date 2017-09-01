# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import exceptions


class MeetingTask(models.Model):
    _name = 'meeting.task'
    _description = 'Meeting task'
    _inherit = ['mail.thread']
    Theme = fields.Char('主题',required=True,help="添加会议主题")
    Lecturer = fields.Char('讲师')
    Docs=fields.Html('简介')
    Time=fields.Datetime('时间',required=True)
    Place=fields.Char('地点',required=True)
    user_id=fields.Many2one('res.users','协调者')
    date_deadline=fields.Datetime('报名截止日期')
    Ppt=fields.Binary("PPT")
    
    user_ids=fields.Many2many('res.users',string='参加人员')
    user_count=fields.Integer('人数',compute='_get_count')
     
    @api.multi
    def register(self):
        user_id=(4,[[self.env.user.id]])
        self.write({'user_ids':[user_id]})
	#self.env.cr.commit()
	#raise exceptions.Warning(self.env.user.name,"报名成功！")
        return True 
      
    @api.multi
    def _get_count(self):
        self.user_count=len(self.user_ids)
        return True





