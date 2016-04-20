# -*- coding: utf-8 -*-
from openerp import api, fields, models


class financial_home(models.Model):
    _name = "financial.home"
    _rec_name = "action"

    sequence = fields.Integer(u'序列')
    action = fields.Many2one('ir.actions.act_window', string='快捷页面', required='1')
    image = fields.Binary(u"显示的图片")
    menu_type = fields.Selection([(u'main', u'主菜单'), (u'top', u'金额汇总'), (u'left', u'快速查看')], string='类型', required="1")
    domain = fields.Char(u'页面的过滤', default='[]')
    note_one = fields.Char(u'第一个显示名称')
    compute_field_one = fields.Many2one('ir.model.fields', string='需要计算的字段')
    note_two = fields.Char(u'显示名称')
    compute_field_two = fields.Many2one('ir.model.fields', string='需要计算的字段')
    compute_type = fields.Selection([(u'sum', u'sum'), (u'average', u'average')], default="sum", string="计算类型")
    context = fields.Char(u'动作的上下文')

    @api.model
    def get_action_url(self):
        action_url_lsit = {'main': [], 'top': [], 'left': []}

        action_list = self.env['financial.home'].search([(1, '=', 1)], order='sequence')
        for action in action_list:
            if action:
                if action.menu_type == 'main':
                    action_url_lsit['main'].append([action.note_one, action.action.view_mode, action.action.res_model, action.action.domain, action.action.id, action.action.context])
                elif action.menu_type == 'top':
                    note = ""
                    res_model_objs = self.env[action.action.res_model].search(eval(action.domain or '[]'))
                    if action.compute_field_one and action.compute_field_two:
                        note = "%s  %s <br\> %s  %s" % (action.note_one, sum([res_model_obj[action.compute_field_one.name] for res_model_obj in res_model_objs]),
                                                        action.note_two, sum([res_model_obj[action.compute_field_two.name] for res_model_obj in res_model_objs]))
                    elif action.compute_field_one or action.compute_field_two:
                        field_compute, note = "", ""
                        if action.compute_field_one:
                            field_compute = action.compute_field_one.name
                            note = action.note_one
                        else:
                            field_compute = action.compute_field_two.name
                            note = action.note_two
                        note = "%s  %s" % (note, sum([res_model_obj[field_compute] for res_model_obj in res_model_objs]))

                    else:
                        note = "%s  %s" % (action.note_one, sum([1 for res_model_obj in res_model_objs]))

                    action_url_lsit['top'].append([note, action.action.view_mode, action.action.res_model, action.domain, action.context])
                else:
                    action_url_lsit['left'].append([action.note_one, action.action.view_mode, action.action.res_model, action.domain, action.context])
        return action_url_lsit
