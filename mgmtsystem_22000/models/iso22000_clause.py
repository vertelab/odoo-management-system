# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Iso22000Clause(models.Model):
    _name = "iso22000.clause"
    _description = "ISO 22000:2018 Clause"
    _order = "sequence, clause_number"
    _rec_name = "display_name"

    name = fields.Char(required=True, translate=True)
    clause_number = fields.Char(
        required=True,
        help="ISO 22000 clause number, e.g. '8.5'",
    )
    display_name = fields.Char(compute="_compute_display_name", store=True)
    description = fields.Text(translate=True)
    parent_id = fields.Many2one(
        "iso22000.clause", "Parent Clause", index=True, ondelete="cascade"
    )
    child_ids = fields.One2many("iso22000.clause", "parent_id", "Child Clauses")
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        help="Clauses are company-specific but typically shared across companies",
    )

    _sql_constraints = [
        (
            "clause_number_uniq",
            "unique(clause_number)",
            "Clause number must be unique!",
        ),
    ]

    @api.depends("clause_number", "name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.clause_number} {rec.name}"
