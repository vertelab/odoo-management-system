# Copyright (C) 2025 Vertel AB
# License AGPL-3.0

from odoo import fields, models


class HrOnboardingTemplate(models.Model):
    _inherit = 'hr.onboarding.template'

    mgmtsystem_standard_ids = fields.Many2many(
        'mgmtsystem.system',
        string='Applicable ISO Standards',
        help='ISO standards that trigger additional onboarding steps',
    )
    include_iso_training = fields.Boolean(
        string='Include ISO Awareness Training',
        default=True,
        help='Automatically add ISO-specific steps when this template is used',
    )
