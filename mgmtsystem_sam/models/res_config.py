# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sam_auto_create_channels = fields.Boolean(
        string="Skapa discuss-kanaler automatiskt",
        config_parameter="mgmtsystem_sam.auto_create_channels",
        default=True,
        help="Skapa automatiskt en discuss-kanal per avdelning för arbetsmiljödiskussioner",
    )
    sam_default_review_month = fields.Selection(
        [
            ("1", "Januari"),
            ("2", "Februari"),
            ("3", "Mars"),
            ("4", "April"),
            ("5", "Maj"),
            ("6", "Juni"),
            ("7", "Juli"),
            ("8", "Augusti"),
            ("9", "September"),
            ("10", "Oktober"),
            ("11", "November"),
            ("12", "December"),
        ],
        string="Månad för årlig uppföljning",
        config_parameter="mgmtsystem_sam.default_review_month",
        default="1",
    )
