# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso22000Prp(models.Model):
    _name = "iso22000.prp"
    _description = "Prerequisite Programme (PRP)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, translate=True)
    category = fields.Selection(
        [
            ("hygiene", "Personal Hygiene"),
            ("cleaning", "Cleaning and Sanitation"),
            ("pest", "Pest Control"),
            ("infrastructure", "Infrastructure and Maintenance"),
            ("supplier", "Supplier Management"),
            ("training", "Training"),
            ("traceability", "Traceability Systems"),
            ("allergen", "Allergen Management"),
            ("waste", "Waste Management"),
            ("other", "Other"),
        ],
        string="PRP Category",
        required=True,
        default="other",
    )
    description = fields.Html(string="Description")
    verification_method = fields.Text(
        string="Verification Method",
        help="How this PRP is verified (e.g., audit, inspection, testing)",
    )
    frequency = fields.Selection(
        [
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("annually", "Annually"),
            ("continuous", "Continuous"),
        ],
        string="Verification Frequency",
        default="monthly",
    )
    responsible_id = fields.Many2one(
        "res.users", string="Responsible Person"
    )
    last_verified = fields.Date(string="Last Verified")
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("inactive", "Inactive"),
        ],
        default="draft",
        tracking=True,
    )
    iso22000_clause_ids = fields.Many2many(
        "iso22000.clause",
        string="ISO 22000 Clauses",
        help="Linked to ISO 22000:2018 clause 8.2",
    )

    def action_activate(self):
        self.write({"state": "active"})

    def action_deactivate(self):
        self.write({"state": "inactive"})
