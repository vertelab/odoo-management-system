# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Iso42001Clause(models.Model):
    _name = "iso42001.clause"
    _description = "ISO 42001:2023 Clause"
    _order = "sequence, clause_number"
    _rec_name = "display_name"

    name = fields.Char(required=True, translate=True)
    clause_number = fields.Char(required=True)
    display_name = fields.Char(compute="_compute_display_name", store=True)
    description = fields.Text(translate=True)
    parent_id = fields.Many2one(
        "iso42001.clause", "Parent Clause", index=True, ondelete="cascade"
    )
    child_ids = fields.One2many("iso42001.clause", "parent_id", "Child Clauses")
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company
    )

    _sql_constraints = [
        ("clause_number_uniq", "unique(clause_number)", "Clause number must be unique!"),
    ]

    @api.depends("clause_number", "name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.clause_number} {rec.name}"
