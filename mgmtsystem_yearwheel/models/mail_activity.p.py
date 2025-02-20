from odoo import models, fields, api


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    year_wheel_id = fields.Many2one('year.wheel', string="Year Wheel")
