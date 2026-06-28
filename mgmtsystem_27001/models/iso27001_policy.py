# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso27001Policy(models.Model):
    _name = "iso27001.policy"
    _description = "Information Security Policy"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_approved desc"

    name = fields.Char(required=True, translate=True)
    description = fields.Html(string="Policy Description")
    date_approved = fields.Date(string="Approved Date")
    date_review = fields.Date(string="Next Review")
    approved_by = fields.Many2one("res.users", string="Approved By")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("archived", "Archived"),
        ],
        default="draft",
        tracking=True,
    )
    iso27001_clause_ids = fields.Many2many(
        "iso27001.clause",
        string="ISO 27001 Clauses",
        help="Linked to ISO 27001:2022 clause 5.2: Information Security Policy",
    )

    def action_approve(self):
        self.write({"state": "active", "date_approved": fields.Date.today()})

    def action_archive(self):
        self.write({"state": "archived"})

    def action_draft(self):
        self.write({"state": "draft"})
