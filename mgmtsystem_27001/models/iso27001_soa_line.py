# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso27001SoaLine(models.Model):
    _name = "iso27001.soa.line"
    _description = "Statement of Applicability Line"
    _order = "control_id"

    soa_id = fields.Many2one("iso27001.soa", required=True, ondelete="cascade")
    control_id = fields.Many2one(
        "mgmtsystem.security.control",
        string="Annex A Control",
        required=True,
    )
    company_id = fields.Many2one(related="soa_id.company_id", store=True)
    applicable = fields.Boolean(
        string="Tillämplig",
        default=True,
        help="Is this control applicable to the organization?",
    )
    implemented = fields.Boolean(
        string="Implementerad",
        help="Is this control already implemented?",
    )
    justification = fields.Text(
        string="Motivering",
        help="Justification for applicability/non-applicability",
    )
    implementation_status = fields.Text(
        string="Implementation Status",
        help="Current implementation status and evidence",
    )
    linked_event_ids = fields.Many2many(
        "mgmtsystem.security.event",
        "iso27001_soa_event_rel",
        "soa_line_id",
        "event_id",
        string="Linked Feared Events",
        help="OCA feared events linked to this control",
    )
    action_ids = fields.Many2many(
        "mgmtsystem.action",
        "iso27001_soa_action_rel",
        "soa_line_id",
        "action_id",
        string="Actions",
        help="Actions related to implementing this control",
    )
