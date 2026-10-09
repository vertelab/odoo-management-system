# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MgmtSystemIsoClause(models.Model):
    """A clause in a management system standard.

    The clause number is unique *within* its standard, not globally:
    clause 5.2 exists in both ISO 9001 and ISO 27001 with different meaning.
    """

    _name = "mgmtsystem.iso.clause"
    _description = "ISO Clause"
    _order = "standard_id, sequence, clause_number"
    _rec_name = "display_name"

    name = fields.Char(required=True, translate=True)
    clause_number = fields.Char(
        required=True,
        help="ISO-klausulnummer, t.ex. '5.2'",
    )
    standard_id = fields.Many2one(
        "mgmtsystem.iso.standard",
        string="Standard",
        required=True,
        ondelete="cascade",
        index=True,
    )
    description = fields.Text(translate=True)
    parent_id = fields.Many2one(
        "mgmtsystem.iso.clause",
        "Förälderklausul",
        index=True,
        ondelete="cascade",
    )
    child_ids = fields.One2many(
        "mgmtsystem.iso.clause",
        "parent_id",
        "Underklausuler",
    )
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        help="Klausuler är företagsspecifika men delas typiskt mellan bolag",
    )

    _sql_constraints = [
        (
            "clause_number_standard_uniq",
            "unique(clause_number, standard_id)",
            "Klausulnumret måste vara unikt inom standarden!",
        ),
    ]

    @api.depends("clause_number", "name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.clause_number} {rec.name}"

    @api.onchange("standard_id")
    def _onchange_standard_id(self):
        """Clear the parent when the standard changes.

        A parent clause belongs to a standard; switching standard would
        otherwise leave a parent from another standard's tree.
        """
        if self.parent_id and self.parent_id.standard_id != self.standard_id:
            self.parent_id = False

    @api.constrains("parent_id", "standard_id")
    def _check_parent_same_standard(self):
        for rec in self:
            if rec.parent_id and rec.parent_id.standard_id != rec.standard_id:
                raise ValidationError(
                    "En klausuls förälder måste tillhöra samma standard."
                )
