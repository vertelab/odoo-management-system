# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo.exceptions import ValidationError
from typing import Any
from odoo import api, exceptions, fields, models, _, Command


class YearWheelWizard(models.Model):
    _name = "year.wheel.wizard"
    _description = 'Year Wheel Wizard'
    _rec_name = 'summary'

    @api.model
    def default_get(self, fields):
        res = super(YearWheelWizard, self).default_get(fields)
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

    user_id = fields.Many2one(
        'res.users', 'Assigned to',
        default=lambda self: self.env.user,
        index=True, required=True)

    _sql_constraints = [
        ('check_wheel_date_validity',
         'CHECK(end_date >= start_date)',
         'This wheel has already ended before it could even start')
    ]

    def action_open_wheel_wizard(self):
        return {
            'name': 'Management Year Wheel',
            'type': 'ir.actions.act_window',
            'res_model': 'year.wheel.wizard',
            'view_mode': 'form',
            'views': [(self.env.ref('mgmtsystem_yearwheel.year_wheel_view_form_popup').id, 'form')],
            'target': 'new',
        }

    @api.onchange('start_date')
    def change_next_activity_date(self):
        self.next_activity_date = self.start_date

    def action_create_year_wheel(self):
        if not self.year_wheel_value():
            raise ValidationError("No value for your activities")

        year_wheel_id = self.env['year.wheel'].create(self.year_wheel_value())

        year_wheel_id.action_create_year_wheel_activity()

        return {
            'name': 'Year Wheel',
            'type': 'ir.actions.act_window',
            'res_model': 'year.wheel',
            'view_mode': 'form',
            'res_id': year_wheel_id.id,
            'views': [(False, 'form')],
        }

    def year_wheel_value(self) -> dict[str, Any]:
        vals = {
            'activity_type_id': self.activity_type_id.id,
            'res_id': self.res_id,
            'res_model': self.res_model,
            'res_model_id': self.res_model_id.id,
            'summary': self.summary,
            'note': self.note,
            'user_id': self.user_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'interval': self.interval,
            'time_unit': self.time_unit,
        }
        return vals
