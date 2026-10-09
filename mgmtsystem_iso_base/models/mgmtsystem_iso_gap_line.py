# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtSystemIsoGapLine(models.Model):
    """One assessed clause in a gap analysis.

    Maturity runs 0–5; an untouched line is level 0.
    """

    _name = "mgmtsystem.iso.gap.line"
    _description = "ISO Gap Analysis Line"
    _order = "clause_id"

    gap_id = fields.Many2one(
        "mgmtsystem.iso.gap", required=True, ondelete="cascade", index=True
    )
    clause_id = fields.Many2one(
        "mgmtsystem.iso.clause",
        string="ISO-klausul",
        required=True,
        ondelete="restrict",
    )
    company_id = fields.Many2one(
        related="gap_id.company_id", store=True, index=True
    )
    maturity_level = fields.Selection(
        [
            ("0", "0 – Saknas"),
            ("1", "1 – Initial"),
            ("2", "2 – Upprepbar"),
            ("3", "3 – Definierad"),
            ("4", "4 – Styrd"),
            ("5", "5 – Optimerad"),
        ],
        string="Mognadsnivå",
        default="0",
    )
    finding = fields.Text(string="Fynd")
    recommendation = fields.Text(string="Rekommendation")
    status = fields.Selection(
        [
            ("open", "Öppen"),
            ("in_progress", "Pågår"),
            ("resolved", "Åtgärdad"),
        ],
        default="open",
    )
