# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    iso27001_clause_ids = fields.Many2many(
        "iso27001.clause",
        "iso27001_action_clause_rel",
        "action_id",
        "clause_id",
        string="ISO 27001 Clauses",
        help="ISO 27001:2022 clauses this action addresses",
    )
