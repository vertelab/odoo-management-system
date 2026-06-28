# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso9001Gap(models.Model):
    _name = "iso9001.gap"
    _description = "ISO 9001 Gap Analysis"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc"

    name = fields.Char(required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    assessed_by = fields.Many2one("res.users", string="Assessed By")
    state = fields.Selection(
        [("draft", "Draft"), ("in_progress", "In Progress"), ("done", "Completed")],
        default="draft",
        tracking=True,
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    line_ids = fields.One2many("iso9001.gap.line", "gap_id", string="Gap Lines")
    notes = fields.Html(string="Notes")

    def action_start(self):
        self.write({"state": "in_progress"})

    def action_done(self):
        self.write({"state": "done"})

    def action_draft(self):
        self.write({"state": "draft"})
