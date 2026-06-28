# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso22000GapLine(models.Model):
    _name = "iso22000.gap.line"
    _description = "ISO 22000 Gap Analysis Line"
    _order = "clause_id"

    gap_id = fields.Many2one("iso22000.gap", required=True, ondelete="cascade")
    clause_id = fields.Many2one(
        "iso22000.clause",
        string="ISO 22000 Clause",
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
