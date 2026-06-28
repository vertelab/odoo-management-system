# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso9001Objective(models.Model):
    _name = "iso9001.objective"
    _description = "Quality Objective"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "deadline desc, name"

    name = fields.Char(required=True, translate=True)
    description = fields.Html(string="Description")
    kpi_description = fields.Char(
        string="KPI Description",
        help="How this objective will be measured (e.g. 'Customer satisfaction score > 85%')",
    )
    target_value = fields.Char(string="Target Value")
    current_value = fields.Char(string="Current Value")
    owner_id = fields.Many2one(
        "res.users",
        string="Responsible",
        help="Person responsible for achieving this objective",
    )
    deadline = fields.Date(string="Deadline")
    iso9001_clause_ids = fields.Many2many(
        "iso9001.clause",
        string="ISO 9001 Clauses",
        help="Linked to ISO 9001:2026 clauses, typically 6.2",
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("achieved", "Achieved"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    def action_activate(self):
        self.write({"state": "active"})

    def action_achieve(self):
        self.write({"state": "achieved"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_draft(self):
        self.write({"state": "draft"})
