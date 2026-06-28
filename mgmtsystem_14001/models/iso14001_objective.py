# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso14001Objective(models.Model):
    _name = "iso14001.objective"
    _description = "Environmental Objective"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "deadline desc, name"

    name = fields.Char(required=True, translate=True)
    description = fields.Html(string="Description")
    kpi_description = fields.Char(string="KPI Description")
    target_value = fields.Char(string="Target Value")
    current_value = fields.Char(string="Current Value")
    owner_id = fields.Many2one("res.users", string="Responsible")
    deadline = fields.Date(string="Deadline")
    iso14001_clause_ids = fields.Many2many(
        "iso14001.clause", string="ISO 14001 Clauses",
        help="Linked to ISO 14001:2026, typically 6.2"
    )
    iso14001_aspect_ids = fields.Many2many(
        "iso14001.aspect", string="Environmental Aspects"
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    state = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("achieved", "Achieved"), ("cancelled", "Cancelled")],
        default="draft", tracking=True
    )

    def action_activate(self):
        self.write({"state": "active"})

    def action_achieve(self):
        self.write({"state": "achieved"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_draft(self):
        self.write({"state": "draft"})
