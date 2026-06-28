# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso22000Emergency(models.Model):
    _name = "iso22000.emergency"
    _description = "Emergency Preparedness / Recall Plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, translate=True)
    scenario = fields.Selection(
        [
            ("recall", "Product Recall"),
            ("withdrawal", "Product Withdrawal"),
            ("contamination", "Contamination Incident"),
            ("allergen", "Allergen Incident"),
            ("fraud", "Food Fraud"),
            ("natural_disaster", "Natural Disaster"),
            ("utility_failure", "Utility Failure"),
            ("other", "Other"),
        ],
        string="Scenario",
        required=True,
    )
    description = fields.Html(string="Scenario Description")
    procedure = fields.Html(
        string="Emergency Procedure",
        help="Step-by-step emergency response procedure",
    )
    responsible_ids = fields.Many2many(
        "res.users",
        string="Emergency Response Team",
    )
    external_contacts = fields.Text(
        string="External Contacts",
        help="Authorities, laboratories, media contacts",
    )
    communication_template = fields.Html(
        string="Communication Template",
        help="Template for public/customer communication during recall",
    )
    last_tested = fields.Date(string="Last Tested/Exercised")
    test_result = fields.Html(string="Test Result")
    test_frequency = fields.Selection(
        [
            ("quarterly", "Quarterly"),
            ("biannual", "Twice a Year"),
            ("annually", "Annually"),
        ],
        string="Test Frequency",
        default="annually",
    )
    next_test_date = fields.Date(string="Next Test Date")
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active — Ready"),
            ("tested", "Tested — Verified"),
            ("outdated", "Needs Review"),
        ],
        default="draft",
        tracking=True,
    )

    def action_activate(self):
        self.write({"state": "active"})

    def action_test_complete(self):
        self.write({
            "state": "tested",
            "last_tested": fields.Date.today(),
        })

    def action_needs_review(self):
        self.write({"state": "outdated"})
