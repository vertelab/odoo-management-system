# Copyright (C) 2025 Vertel AB
# License AGPL-3.0

from odoo import fields, models


class HrEmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'

    certification_date = fields.Date(string='Certification Date')
    expiration_date = fields.Date(string='Expiration Date')
    certificate_document_id = fields.Many2one(
        'ir.attachment',
        string='Certificate Document',
    )
