# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso27001GapLine(models.Model):
    _name = "iso27001.gap.line"
    _description = "ISO 27001 Gap Analysis Line"
    _order = "control_id"

    gap_id = fields.Many2one("iso27001.gap", required=True, ondelete="cascade")
    control_id = fields.Many2one(
        "mgmtsystem.security.control",
        string="Annex A Control",
        required=True,
    )
    company_id = fields.Many2one(related="gap_id.company_id", store=True)
    maturity_level = fields.Selection(
        [
            ("0", "0 - Non-existent"),
            ("1", "1 - Initial"),
            ("2", "2 - Repeatable"),
            ("3", "3 - Defined"),
            ("4", "4 - Managed"),
            ("5", "5 - Optimized"),
        ],
        string="Maturity Level",
        default="0",
    )
    finding = fields.Text(string="Finding")
    recommendation = fields.Text(string="Recommendation")
    status = fields.Selection(
        [
            ("open", "Open"),
            ("in_progress", "In Progress"),
            ("resolved", "Resolved"),
        ],
        default="open",
    )
