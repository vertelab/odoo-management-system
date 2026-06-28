# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso9001GapLine(models.Model):
    _name = "iso9001.gap.line"
    _description = "ISO 9001 Gap Analysis Line"
    _order = "clause_id"

    gap_id = fields.Many2one("iso9001.gap", required=True, ondelete="cascade")
    clause_id = fields.Many2one(
        "iso9001.clause",
        string="ISO 9001 Clause",
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
