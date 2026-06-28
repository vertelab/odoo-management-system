# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso14001Aspect(models.Model):
    _name = "iso14001.aspect"
    _description = "Environmental Aspect"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, translate=True)
    activity = fields.Char(
        string="Activity / Product / Service",
        help="The activity, product, or service that gives rise to this aspect",
    )
    aspect_type = fields.Selection(
        [
            ("emission", "Emission to Air"),
            ("discharge", "Discharge to Water"),
            ("waste", "Waste"),
            ("resource", "Resource Use"),
            ("energy", "Energy Use"),
            ("noise", "Noise"),
            ("landuse", "Land Use"),
            ("biodiversity", "Biodiversity Impact"),
            ("other", "Other"),
        ],
        string="Aspect Type",
        default="other",
    )
    significance = fields.Selection(
        [("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")],
        string="Significance",
        default="low",
    )
    life_cycle_stage = fields.Selection(
        [
            ("raw_material", "Raw Material Acquisition"),
            ("design", "Design"),
            ("production", "Production"),
            ("transport", "Transport/Delivery"),
            ("use", "Use"),
            ("end_of_life", "End-of-Life"),
        ],
        string="Life Cycle Stage",
    )
    controls = fields.Text(string="Existing Controls")
    iso14001_clause_ids = fields.Many2many(
        "iso14001.clause", string="ISO 14001 Clauses",
        help="Linked to ISO 14001:2026, typically 6.1.2"
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    state = fields.Selection(
        [("draft", "Draft"), ("evaluated", "Evaluated"), ("controlled", "Controlled")],
        default="draft", tracking=True
    )

    def action_evaluate(self):
        self.write({"state": "evaluated"})

    def action_control(self):
        self.write({"state": "controlled"})
