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
            'view_mode': 'tree, form',
            'views': [(False, 'tree'), (False, 'form')],
            'domain': [('year_wheel_id', '=', self.id)]
        }

    user_id = fields.Many2one(
        'res.users', 'Assigned to',
        default=lambda self: self.env.user,
        index=True, required=True)

    _sql_constraints = [
        # Required on a Many2one reference field is not sufficient as actually
        # writing 0 is considered as a valid value, because this is an integer field.
        # We therefore need a specific constraint check.
        ('check_res_id_is_set',
         'CHECK(res_id IS NOT NULL AND res_id !=0 )',
         'Activities have to be linked to records with a not null res_id.')
    ]

    def action_open_wheel(self):
        return {
            'name': 'Management Year Wheel',
            'type': 'ir.actions.act_window',
            'res_model': 'year.wheel',
            'view_mode': 'form',
            'views': [(self.env.ref('mgmtsystem_yearwheel.year_wheel_view_form_popup').id, 'form')],
            'target': 'new',
        }

    @api.depends('res_model', 'res_id')
    def _compute_res_name(self):
        for activity in self:
            activity.res_name = activity.res_model and \
                                self.env[activity.res_model].browse(activity.res_id).display_name

    def action_create_year_wheel_activity(self):
        if not self.mail_activity_value():
            raise ValidationError("No value for your activities")

        if self.start_date == fields.Date.today():
            self.env['mail.activity'].create(self.mail_activity_value())

    def _cron_action_create_next_activity(self):
        wheel_ids = self.env['year.wheel'].search([
            ('end_date', '>=', fields.Date.today()),
            ('start_date', '<=', fields.Date.today()),
            ('next_wheel_date', '<=', fields.Date.today()),
        ])
        for wheel in wheel_ids:
            while wheel.next_wheel_date < fields.Date.today():
                mail_activity_id = self.env['mail.activity'].create(wheel.mail_activity_value())
                if mail_activity_id:
                    wheel.next_wheel_date = self._switch_time_unit(
                        time_unit=wheel.time_unit, interval=wheel.interval, date_field=wheel.next_wheel_date
                    )

    def _switch_time_unit(self, time_unit, interval, date_field) -> relativedelta | date | datetime:
        match time_unit:
            case "days":
                return date_field + relativedelta(days=interval)
            case "weeks":
                return date_field + relativedelta(weeks=interval)
            case "months":
                return date_field + relativedelta(months=interval)
            case "years":
                return date_field + relativedelta(years=interval)

    def mail_activity_value(self) -> dict[str, Any]:
        date_deadline = self._switch_time_unit(
            time_unit=self.activity_due_interval, interval=self.activity_due_in, date_field=self.next_wheel_date
        )
        if self.copy_reference:
            template_record = self.env[self.res_model].browse(self.res_id)
            copy_record = template_record.copy()
            copy_record.name = f"{template_record.name}-{date_deadline}"
            self.run_code(copy_record)
            res_id = copy_record.id
        else:
            res_id = self.res_id
        next_activities_values = {
            'activity_type_id': self.activity_wheel_type_id.id,
            'res_id': res_id,
            'res_model': self.res_model,
            'res_model_id': self.res_model_id.id,
            'summary': self.summary,
            'note': self.note,
            'user_id': self.user_id.id,
            'date_deadline': date_deadline,
            'year_wheel_id': self.id
        }
        return next_activities_values

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('start_date') > val.get('end_date'):
                raise ValidationError(_('This wheel has already ended before it could even start'))
        res = super(YearWheel, self).create(vals_list)
        for rec in res:
            rec.action_create_year_wheel_activity()
        return res

    def write(self, vals):
        res = super(YearWheel, self).write(vals)
        if self.start_date > self.end_date:
            raise ValidationError(_('This wheel has already ended before it could even start'))
        return res

    @api.onchange('start_date', 'interval', 'time_unit', 'next_wheel_date')
    def onchange_start_date(self):
        if not self.activity_ids:
            self.next_wheel_date = self._switch_time_unit(
                time_unit=self.time_unit, interval=self.interval, date_field=self.start_date
            )
