# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QualityPoint(models.Model):
    _inherit = "quality.point"

    iso_clause_ids = fields.Many2many(
        "mgmtsystem.iso.clause",
        "quality_point_iso_clause_rel",
        "point_id",
        "clause_id",
        string="ISO-klausuler",
        help="De ISO-klausuler som kräver denna kontroll. Gör att det vid en "
             "revision går att visa varför kontrollen finns.",
    )
