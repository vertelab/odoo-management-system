# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz

from collections import defaultdict
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Any

from odoo import api, exceptions, fields, models, _, Command


class YearWheel(models.Model):
    _name = "year.wheel"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _description = 'Year Wheel'
    _order = 'end_date ASC, id ASC'
    _rec_name = 'summary'
    
    code = fields.Text(
        string="Code",
        default="""# You have access to the variable `record` inside this code block.
# `record` represents the current record are planing an activity on.
#
# Example: set a field value
# record.name = "test"
#
# Example: call a method defined on the model
# record.test_func()
#
# Write any custom Python logic below:
        """
        )

    def run_code(self, record):
        local_vars = {'record': record}
        try:
            exec(record.code, {}, local_vars)
        except Exception as e:
            # handle or log error appropriately
            raise e

    @api.model
    def _selection_target_model(self):
        domain = [('transient', '=', False), ('is_mail_activity', '=', True)]
        return [(model.model, model.name) for model in self.env['ir.model'].sudo().search(domain)]

    @api.model
    def default_get(self, fields):
        res = super(YearWheel, self).default_get(fields)
        if not fields or 'res_model_id' in fields and res.get('res_model'):
            res['res_model_id'] = self.env['ir.model']._get(res['res_model']).id
        return res

    @api.depends('res_model_id')
    def _compute_resource_ref(self):
        for rec in self:
            if rec.res_model_id:
                rec.resource_ref = '%s,%s' % (rec.res_model, rec.res_id)
            else:
                rec.resource_ref = False

    @api.onchange('resource_ref')
    def onchange_resource_ref(self):
        if self.resource_ref:
            self.res_id = self.resource_ref.id
            self.res_model_id = self.env['ir.model'].search([('model', '=', self.resource_ref._name)], limit=1).id,

    res_model_id = fields.Many2one(
        'ir.model', 'Document Model',
        index=True, ondelete='cascade', required=True,
        domain=[('transient', '=', False), ('is_mail_activity', '=', True)])

    res_model = fields.Char(
        'Related Document Model',
        index=True, related='res_model_id.model', compute_sudo=True, store=True, readonly=True)

    resource_ref = fields.Reference(string='Record Reference',
                                    selection=_selection_target_model,
                                    compute=_compute_resource_ref, readonly=False, required=True)
    copy_reference = fields.Boolean(string="Create a copy of reference", help="if set to true it will copy the reference and create an activity on it.")
    res_id = fields.Many2oneReference(string='Related Document ID', index=True, model_field='res_model')
    res_name = fields.Char(
        'Document Name', compute='_compute_res_name', compute_sudo=True, store=True,
        readonly=True)

    activity_wheel_type_id = fields.Many2one(
        'mail.activity.type', string='Activity Type',
        domain="['|', ('res_model', '=', False), ('res_model', '=', res_model)]", ondelete='restrict',
    )

    summary = fields.Char('Summary')
    note = fields.Html('Note', sanitize_style=True)

    start_date = fields.Date('Wheel Start Date', index=True, required=True, default=fields.Date.context_today)
    end_date = fields.Date('Wheel End Date', index=True, required=True, default=fields.Date.context_today)

    activity_due_in = fields.Integer('Activity Due In', default=1, store=True)
    activity_due_interval = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years')
    ], default='days')

    next_wheel_date = fields.Date(
        string='Next Wheel Date', readonly=True, store=True
    )

    interval = fields.Integer(string="Wheel Interval", default=1, store=True)
    time_unit = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years')
    ], default='days')

    activity_ids = fields.One2many('mail.activity', 'year_wheel_id', string="Activities")

    @api.depends('activity_ids')
    def _compute_activity_count(self):
        for rec in self:
            rec.activity_count = len(rec.activity_ids)

    activity_count = fields.Float(string="Activities Count", compute=_compute_activity_count)

    def action_view_activities(self):
        return {
            'name': 'Year Wheel Activities',
            'type': 'ir.actions.act_window',
            'res_model': 'mail.activity',
