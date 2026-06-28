# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Iso22000Hazard(models.Model):
    _name = "iso22000.hazard"
    _description = "Food Safety Hazard Analysis"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    haccp_id = fields.Many2one(
        "iso22000.haccp",
        string="HACCP Plan",
        required=True,
        ondelete="cascade",
    )
    process_step = fields.Char(
        string="Process Step",
        help="Step in the flow diagram where this hazard occurs",
    )
    hazard_type = fields.Selection(
        [
            ("biological", "Biological"),
            ("chemical", "Chemical"),
            ("physical", "Physical"),
            ("allergenic", "Allergenic"),
            ("radiological", "Radiological"),
        ],
        string="Hazard Type",
        required=True,
        default="biological",
    )
    hazard_description = fields.Text(
        string="Hazard Description",
        help="Describe the hazard in detail",
    )
    probability = fields.Selection(
        [
            ("1", "1 - Very Low"),
            ("2", "2 - Low"),
            ("3", "3 - Medium"),
            ("4", "4 - High"),
            ("5", "5 - Very High"),
        ],
        string="Probability",
        default="3",
    )
    severity = fields.Selection(
        [
            ("1", "1 - Minor"),
            ("2", "2 - Moderate"),
            ("3", "3 - Serious"),
            ("4", "4 - Severe"),
            ("5", "5 - Critical"),
        ],
        string="Severity",
        default="3",
    )
    risk_level = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("critical", "Critical"),
        ],
        string="Risk Level",
        compute="_compute_risk_level",
        store=True,
    )
    control_measure = fields.Text(
        string="Control Measure",
        help="Existing or proposed control measure",
    )
    is_ccp = fields.Boolean(
        string="Is CCP?",
        help="Is this hazard controlled by a Critical Control Point?",
    )
    justification = fields.Text(
        string="CCP Justification",
        help="Justification for CCP/non-CCP decision",
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("identified", "Identified"),
            ("assessed", "Risk Assessed"),
            ("controlled", "Controlled"),
            ("reviewed", "Reviewed"),
        ],
        default="identified",
        tracking=True,
    )

    @api.depends("probability", "severity")
    def _compute_risk_level(self):
        for rec in self:
            prob = int(rec.probability) if rec.probability else 3
            sev = int(rec.severity) if rec.severity else 3
            score = prob * sev
            if score >= 20:
                rec.risk_level = "critical"
            elif score >= 12:
                rec.risk_level = "high"
            elif score >= 6:
                rec.risk_level = "medium"
            else:
                rec.risk_level = "low"

    def action_assess(self):
        self.write({"state": "assessed"})

    def action_control(self):
        self.write({"state": "controlled"})

    def action_review(self):
        self.write({"state": "reviewed"})
