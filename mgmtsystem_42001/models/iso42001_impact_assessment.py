# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso42001ImpactAssessment(models.Model):
    _name = "iso42001.impact.assessment"
    _description = "AI Impact Assessment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_assessed desc"

    aisystem_id = fields.Many2one(
        "iso42001.aisystem", string="AI System", required=True, ondelete="cascade"
    )
    fairness = fields.Selection(
        [("1", "1 - High Bias Risk"), ("2", "2"), ("3", "3 - Moderate"),
         ("4", "4"), ("5", "5 - Fair")],
        string="Fairness", default="3",
        help="Assessment of fairness and non-discrimination"
    )
    transparency = fields.Selection(
        [("1", "1 - Opaque"), ("2", "2"), ("3", "3 - Moderate"),
         ("4", "4"), ("5", "5 - Transparent")],
        string="Transparency", default="3",
    )
    privacy = fields.Selection(
        [("1", "1 - High Privacy Risk"), ("2", "2"), ("3", "3 - Moderate"),
         ("4", "4"), ("5", "5 - Privacy-Preserving")],
        string="Privacy", default="3",
    )
    safety = fields.Selection(
        [("1", "1 - Unsafe"), ("2", "2"), ("3", "3 - Moderate"),
         ("4", "4"), ("5", "5 - Safe")],
        string="Safety", default="3",
    )
    bias_mitigation = fields.Text(
        string="Bias Mitigation Measures",
        help="Describe measures to identify and mitigate bias"
    )
    human_oversight = fields.Selection(
        [("none", "No Human Oversight"), ("in_loop", "Human-in-the-Loop"),
         ("on_loop", "Human-on-the-Loop"), ("in_command", "Human-in-Command")],
        string="Human Oversight Level", default="on_loop",
    )
    environmental_impact = fields.Text(
        string="Environmental Impact",
        help="Energy consumption, carbon footprint, resource usage"
    )
    societal_impact = fields.Text(
        string="Societal Impact",
        help="Employment, accessibility, social equity considerations"
    )
    date_assessed = fields.Date(
        required=True, default=fields.Date.context_today
    )
    assessed_by = fields.Many2one("res.users", string="Assessed By")
    company_id = fields.Many2one(related="aisystem_id.company_id", store=True)
    state = fields.Selection(
        [("draft", "Draft"), ("in_review", "In Review"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="draft", tracking=True
    )
    notes = fields.Html(string="Assessment Notes")

    def action_review(self):
        self.write({"state": "in_review"})

    def action_approve(self):
        self.write({"state": "approved"})

    def action_reject(self):
        self.write({"state": "rejected"})
