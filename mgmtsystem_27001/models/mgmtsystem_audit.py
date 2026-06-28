# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemAudit(models.Model):
    _inherit = "mgmtsystem.audit"

    iso27001_clause_ids = fields.Many2many(
        "iso27001.clause",
        "iso27001_audit_clause_rel",
        "audit_id",
        "clause_id",
        string="ISO 27001 Clauses",
        help="ISO 27001:2022 clauses covered by this audit",
    )
    iso27001_control_ids = fields.Many2many(
        "mgmtsystem.security.control",
        "iso27001_audit_control_rel",
        "audit_id",
        "control_id",
        string="Annex A Controls",
        help="Annex A controls verified in this audit",
    )
