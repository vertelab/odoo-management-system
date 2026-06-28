# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Iso27001Soa(models.Model):
    _name = "iso27001.soa"
    _description = "Statement of Applicability"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc"

    name = fields.Char(required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    approved_by = fields.Many2one("res.users", string="Godkänd av")
    date_approved = fields.Date(string="Godkänt datum")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("approved", "Approved"),
            ("archived", "Archived"),
        ],
        default="draft",
        tracking=True,
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    line_ids = fields.One2many("iso27001.soa.line", "soa_id", string="SoA Lines")
    notes = fields.Html(string="Notes")

    def action_approve(self):
        self.write({"state": "approved", "date_approved": fields.Date.today()})

    def action_archive(self):
        self.write({"state": "archived"})

    def action_draft(self):
        self.write({"state": "draft"})
