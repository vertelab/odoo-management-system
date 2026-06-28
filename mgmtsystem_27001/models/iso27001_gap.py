# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso27001Gap(models.Model):
    _name = "iso27001.gap"
    _description = "ISO 27001 Gap Analysis"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc"

    name = fields.Char(required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    assessed_by = fields.Many2one("res.users", string="Bedömd av")
    state = fields.Selection(
        [("draft", "Draft"), ("in_progress", "In Progress"), ("done", "Completed")],
        default="draft",
        tracking=True,
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    line_ids = fields.One2many("iso27001.gap.line", "gap_id", string="Gap Lines")

    def action_start(self):
        """Start the analysis: generate lines for all Annex A controls."""
        self.ensure_one()
        Control = self.env["mgmtsystem.security.control"]
        controls = Control.search(
            [("control_ref", "!=", False)], order="control_ref"
        )
        lines = []
        existing_control_ids = self.line_ids.mapped("control_id").ids
        for control in controls:
            if control.id not in existing_control_ids:
                lines.append(
                    (
                        0,
                        0,
                        {
                            "control_id": control.id,
                            "maturity_level": "0",
                            "status": "open",
                        },
                    )
                )
        if lines:
            self.write({"line_ids": lines})
        self.write({"state": "in_progress"})

    def action_complete(self):
        self.write({"state": "done"})
