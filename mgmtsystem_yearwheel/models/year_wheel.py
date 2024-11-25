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
    _description = 'Year Wheel'
    _order = 'end_date ASC, id ASC'
    _rec_name = 'summary'

    @api.model
    def default_get(self, fields):
        res = super(YearWheel, self).default_get(fields)
        if not fields or 'res_model_id' in fields and res.get('res_model'):
            res['res_model_id'] = self.env['ir.model']._get(res['res_model']).id
        return res

    @api.model
    def _default_activity_type(self):
        default_vals = self.default_get(['res_model_id', 'res_model'])
        if not default_vals.get('res_model_id'):
            return False

        current_model = self.env["ir.model"].sudo().browse(default_vals['res_model_id']).model
        return self._default_activity_type_for_model(current_model)

    @api.model
    def _default_activity_type_for_model(self, model):
        todo_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mail_activity_data_todo', raise_if_not_found=False)
        activity_type_todo = self.env['mail.activity.type'].browse(todo_id) if todo_id else self.env[
            'mail.activity.type']
        if activity_type_todo and activity_type_todo.active and \
                (activity_type_todo.res_model == model or not activity_type_todo.res_model):
            return activity_type_todo
        activity_type_model = self.env['mail.activity.type'].search([('res_model', '=', model)], limit=1)
        if activity_type_model:
            return activity_type_model
        activity_type_generic = self.env['mail.activity.type'].search([('res_model', '=', False)], limit=1)
        return activity_type_generic

    # owner
    res_model_id = fields.Many2one(
        'ir.model', 'Document Model',
        index=True, ondelete='cascade', required=True)
    res_model = fields.Char(
        'Related Document Model',
        index=True, related='res_model_id.model', compute_sudo=True, store=True, readonly=True)
    res_id = fields.Many2oneReference(string='Related Document ID', index=True, model_field='res_model')
    res_name = fields.Char(
        'Document Name', compute='_compute_res_name', compute_sudo=True, store=True,
        readonly=True)
    # activity
    activity_type_id = fields.Many2one(
        'mail.activity.type', string='Activity Type',
        domain="['|', ('res_model', '=', False), ('res_model', '=', res_model)]", ondelete='restrict',
        default=_default_activity_type)

    summary = fields.Char('Summary')
    note = fields.Html('Note', sanitize_style=True)

    start_date = fields.Date('Start Date', index=True, required=True, default=fields.Date.context_today)
    end_date = fields.Date('Due Date', index=True, required=True, default=fields.Date.context_today)

    next_activity_date = fields.Date('Next Date', index=True, required=True, default=fields.Date.context_today)

    interval = fields.Integer(string="Interval", default=1, store=True)
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
            ('next_activity_date', '=', fields.Date.today()),
        ])
        for wheel in wheel_ids:
            mail_activity_id = self.env['mail.activity'].create(wheel.mail_activity_value())
            if mail_activity_id:
                wheel.next_activity_date = self._switch_time_unit(wheel)

    def _switch_time_unit(self, wheel) -> relativedelta | date | datetime:
        time_unit = wheel.time_unit
        match time_unit:
            case "days":
                return wheel.next_activity_date + relativedelta(days=wheel.interval)
            case "weeks":
                return wheel.next_activity_date + relativedelta(weeks=wheel.interval)
            case "months":
                return wheel.next_activity_date + relativedelta(months=wheel.interval)
            case "years":
                return wheel.next_activity_date + relativedelta(years=wheel.interval)

    def mail_activity_value(self) -> dict[str, Any]:
        next_activities_values = {
            'activity_type_id': self.activity_type_id.id,
            'res_id': self.res_id,
            'res_model': self.res_model,
            'res_model_id': self.res_model_id.id,
            'summary': self.summary,
            'note': self.note,
            'user_id': self.user_id.id,
            'date_deadline': self.next_activity_date,
            'year_wheel_id': self.id
        }
        return next_activities_values
