# Copyright (C) 2025 Vertel AB
# License AGPL-3.0

from odoo import fields, models


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    mgmtsystem_standard_id = fields.Many2one(
        'mgmtsystem.system',
        string='ISO Standard',
        help='Linked ISO management system standard',
    )
    certification_name = fields.Char(
        string='Certification Name',
        help='Certificate awarded on completion, e.g. "ISO 9001 Awareness"',
    )
