# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso22000Flow(models.Model):
    _name = "iso22000.flow"
    _description = "Process Flow Diagram"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, translate=True)
    description = fields.Html(string="Description")
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        help="Product this flow diagram covers",
    )
    diagram = fields.Binary(string="Flow Diagram Image")
    diagram_filename = fields.Char()
    steps = fields.Text(
        string="Process Steps",
        help="List all process steps in order (one per line)",
    )
    verified_by = fields.Many2one("res.users", string="Verified By")
    verification_date = fields.Date(string="On-site Verification Date")
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("verified", "Verified"),
            ("outdated", "Outdated"),
        ],
        default="draft",
        tracking=True,
    )

    def action_verify(self):
        self.write({
            "state": "verified",
            "verification_date": fields.Date.today(),
            "verified_by": self.env.user.id,
        })

    def action_outdated(self):
        self.write({"state": "outdated"})
