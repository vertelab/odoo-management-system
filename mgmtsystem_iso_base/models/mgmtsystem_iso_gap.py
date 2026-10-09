# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtSystemIsoGap(models.Model):
    """A gap analysis run against one standard.

    The analysis carries one line per clause. Standards whose gap is
    control-based rather than clause-based (e.g. ISO 27001 Annex A) extend
    the line model in their own shell module — the core stays clause-oriented.
    """

    _name = "mgmtsystem.iso.gap"
    _description = "ISO Gap Analysis"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc"

    name = fields.Char(required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    assessed_by = fields.Many2one("res.users", string="Bedömd av")
    standard_id = fields.Many2one(
        "mgmtsystem.iso.standard",
        string="Standard",
        required=True,
        ondelete="restrict",
        index=True,
    )
    state = fields.Selection(
        [
            ("draft", "Utkast"),
            ("in_progress", "Pågår"),
            ("done", "Klar"),
        ],
        default="draft",
        tracking=True,
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    line_ids = fields.One2many(
        "mgmtsystem.iso.gap.line", "gap_id", string="Gap-rader"
    )
    notes = fields.Html(string="Anteckningar")

    def action_start(self):
        self.write({"state": "in_progress"})

    def action_done(self):
        self.write({"state": "done"})

    def action_draft(self):
        self.write({"state": "draft"})
