# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Iso14001Impact(models.Model):
    _name = "iso14001.impact"
    _description = "Environmental Impact"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    aspect_id = fields.Many2one(
        "iso14001.aspect", string="Environmental Aspect", required=True, ondelete="cascade"
    )
    impact_type = fields.Selection(
        [
            ("climate", "Climate Change"),
            ("air", "Air Quality"),
            ("water", "Water Quality"),
            ("soil", "Soil Contamination"),
            ("biodiversity", "Biodiversity Loss"),
            ("resource", "Resource Depletion"),
            ("health", "Human Health"),
            ("other", "Other"),
        ],
        string="Impact Type",
        default="other",
    )
    severity = fields.Selection(
        [("1", "1 - Negligible"), ("2", "2 - Minor"), ("3", "3 - Moderate"),
         ("4", "4 - Major"), ("5", "5 - Catastrophic")],
        string="Severity", default="1"
    )
    likelihood = fields.Selection(
        [("1", "1 - Rare"), ("2", "2 - Unlikely"), ("3", "3 - Possible"),
         ("4", "4 - Likely"), ("5", "5 - Almost Certain")],
        string="Likelihood", default="1"
    )
    risk_level = fields.Selection(
        [("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")],
        string="Risk Level", compute="_compute_risk_level", store=True
    )
    company_id = fields.Many2one(related="aspect_id.company_id", store=True)

    @api.depends("severity", "likelihood")
    def _compute_risk_level(self):
        for rec in self:
            try:
                score = int(rec.severity) * int(rec.likelihood)
            except (TypeError, ValueError):
                score = 1
            if score <= 4:
                rec.risk_level = "low"
            elif score <= 9:
                rec.risk_level = "medium"
            elif score <= 16:
                rec.risk_level = "high"
            else:
                rec.risk_level = "critical"
