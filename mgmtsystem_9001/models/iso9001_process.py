# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso9001Process(models.Model):
    _name = "iso9001.process"
    _description = "Quality Management Process"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    description = fields.Html(string="Description")
    sequence = fields.Integer(default=10)
    process_type = fields.Selection(
        [
            ("management", "Management Process"),
            ("core", "Core Process"),
            ("support", "Support Process"),
        ],
        string="Process Type",
        default="core",
    )
    inputs = fields.Text(string="Inputs", help="What goes into the process")
    outputs = fields.Text(string="Outputs", help="What comes out of the process")
    resources = fields.Text(string="Resources", help="Required resources")
    kpi_description = fields.Text(
        string="KPIs",
        help="Key Performance Indicators for this process",
    )
    responsible_id = fields.Many2one(
        "res.users",
        string="Process Owner",
    )
    iso9001_clause_ids = fields.Many2many(
        "iso9001.clause",
        string="ISO 9001 Clauses",
        help="Linked to ISO 9001:2026 clauses, typically 4.4, 8.1",
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
            ("inactive", "Inactive"),
        ],
        default="draft",
        tracking=True,
    )

    def action_activate(self):
        self.write({"state": "active"})

    def action_deactivate(self):
        self.write({"state": "inactive"})
