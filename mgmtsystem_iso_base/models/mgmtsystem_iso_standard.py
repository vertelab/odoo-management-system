# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtSystemIsoStandard(models.Model):
    """A management system standard the organisation works against.

    Standards are data, not models: ISO 9001, 14001, 22000, 27001, 42001,
    45001 and any future standard share one clause model and one gap model,
    distinguished by ``standard_id``.
    """

    _name = "mgmtsystem.iso.standard"
    _description = "ISO Standard"
    _order = "sequence, code"
    _rec_name = "display_name"

    name = fields.Char(
        required=True,
        translate=True,
        help="Standardens namn, t.ex. 'Kvalitetsledning'",
    )
    code = fields.Char(
        required=True,
        help="Standardens beteckning, t.ex. 'ISO 9001'",
    )
    version = fields.Char(
        help="Standardens utgåva, t.ex. '2015' eller '2026'",
    )
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        help="Standarden är företagsspecifik men delas typiskt mellan bolag",
    )
    clause_ids = fields.One2many(
        "mgmtsystem.iso.clause",
        "standard_id",
        string="Klausuler",
    )
    clause_count = fields.Integer(
        compute="_compute_clause_count",
        string="# Klausuler",
    )

    _sql_constraints = [
        (
            "code_uniq",
            "unique(code)",
            "Standardens beteckning måste vara unik!",
        ),
    ]

    def _compute_display_name(self):
        for rec in self:
            parts = [rec.code or "", rec.name or ""]
            label = " – ".join(p for p in parts if p)
            if rec.version:
                label = f"{label} ({rec.version})"
            rec.display_name = label

    def _compute_clause_count(self):
        clause_data = self.env["mgmtsystem.iso.clause"]._read_group(
            [("standard_id", "in", self.ids)], ["standard_id"], ["__count"]
        )
        result = {standard.id: count for standard, count in clause_data}
        for rec in self:
            rec.clause_count = result.get(rec.id, 0)
