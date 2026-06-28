# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso22000Haccp(models.Model):
    _name = "iso22000.haccp"
    _description = "HACCP Plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, translate=True)
    description = fields.Html(string="Description")
    product_ids = fields.Many2many(
        "product.product",
        string="Products",
        help="Products covered by this HACCP plan",
    )
    flow_id = fields.Many2one(
        "iso22000.flow",
        string="Flow Diagram",
        help="Linked process flow diagram",
    )
    hazard_ids = fields.One2many(
        "iso22000.hazard",
        "haccp_id",
        string="Hazard Analysis",
    )
    ccp_ids = fields.One2many(
        "iso22000.ccp",
        "haccp_id",
        string="Critical Control Points",
    )
    validation_date = fields.Date(string="Validation Date")
    validation_by = fields.Many2one("res.users", string="Validated By")
    review_date = fields.Date(string="Next Review Date")
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("review", "Under Review"),
            ("archived", "Archived"),
        ],
        default="draft",
        tracking=True,
    )
    notes = fields.Html(string="Notes")

    def action_activate(self):
        self.write({"state": "active"})

    def action_review(self):
        self.write({"state": "review"})

    def action_archive(self):
        self.write({"state": "archived"})
