# Copyright (C) 2025 Vertel AB
# License AGPL-3.0

from odoo import fields, models


class HrSkill(models.Model):
    _inherit = 'hr.skill'

    mgmtsystem_standard_id = fields.Many2one(
        'mgmtsystem.system',
        string='ISO Standard',
        help='Linked ISO management system standard',
    )
    is_certification = fields.Boolean(
        string='Is Certification',
        help='This skill represents a formal certification',
    )
