# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SamPolicy(models.Model):
    _name = "sam.policy"
    _description = "Arbetsmiljöpolicy"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_approved desc"

    name = fields.Char(required=True, translate=True)
    description = fields.Html(string="Policybeskrivning")
    date_approved = fields.Date(string="Godkänd datum")
    date_review = fields.Date(string="Nästa översyn")
    approved_by = fields.Many2one(
        "hr.employee",
        string="Godkänd av",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Företag",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Utkast"),
            ("active", "Aktiv"),
            ("archived", "Arkiverad"),
        ],
        default="draft",
        tracking=True,
    )
    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', '=', '5.2')]",
        help="Kopplas till ISO 45001 klausul 5.2: Arbetsmiljöpolicy",
    )

    def action_approve(self):
        self.write({"state": "active", "date_approved": fields.Date.today()})

    def action_archive(self):
        self.write({"state": "archived"})

    def action_draft(self):
        self.write({"state": "draft"})
