# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso42001AiSystem(models.Model):
    _name = "iso42001.aisystem"
    _description = "AI System Register"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, translate=True)
    system_type = fields.Selection(
        [
            ("chatbot", "Chatbot / Virtual Assistant"),
            ("recommendation", "Recommendation System"),
            ("classification", "Classification / Categorization"),
            ("prediction", "Prediction / Forecasting"),
            ("generation", "Generative AI"),
            ("computer_vision", "Computer Vision"),
            ("nlp", "Natural Language Processing"),
            ("decision_support", "Decision Support"),
            ("automation", "Autonomous System"),
            ("other", "Other"),
        ],
        string="System Type", required=True,
    )
    purpose = fields.Text(string="Purpose", required=True)
    risk_level = fields.Selection(
        [
            ("low", "Low Risk"),
            ("medium", "Medium Risk"),
            ("high", "High Risk"),
            ("critical", "Critical Risk"),
        ],
        string="Risk Level", default="low", tracking=True,
    )
    data_sources = fields.Text(
        string="Data Sources",
        help="Describe the data sources used by this AI system"
    )
    ai_technologies = fields.Text(
        string="AI Technologies",
        help="E.g. LLM, neural networks, decision trees, etc."
    )
    owner_id = fields.Many2one("res.users", string="System Owner")
    documented_information = fields.Html(
        string="Documented Information",
        help="Technical documentation, model cards, etc."
    )
    iso42001_clause_ids = fields.Many2many(
        "iso42001.clause", string="ISO 42001 Clauses"
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("development", "In Development"),
            ("validation", "Validation"),
            ("deployed", "Deployed"),
            ("retired", "Retired"),
        ],
        default="draft", tracking=True,
    )

    def action_develop(self):
        self.write({"state": "development"})

    def action_validate(self):
        self.write({"state": "validation"})

    def action_deploy(self):
        self.write({"state": "deployed"})

    def action_retire(self):
        self.write({"state": "retired"})
