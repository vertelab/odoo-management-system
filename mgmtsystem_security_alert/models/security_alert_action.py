# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SecurityAlertAction(models.Model):
    _name = "security.alert.action"
    _description = "Security Alert - Action Link"
    _order = "alert_id, action_id"

    alert_id = fields.Many2one(
        "security.alert",
        string="Security Alert",
        required=True,
        ondelete="cascade",
    )
    action_id = fields.Many2one(
        "mgmtsystem.action",
        string="Action",
        required=True,
        ondelete="cascade",
    )
    control_id = fields.Many2one(
        "mgmtsystem.security.control",
        string="ISO 27001 Control",
    )
    company_id = fields.Many2one(
        "res.company",
        related="alert_id.company_id",
        store=True,
    )
