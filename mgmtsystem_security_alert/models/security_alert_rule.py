# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SecurityAlertRule(models.Model):
    _name = "security.alert.rule"
    _description = "Security Alert Filtering Rule"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    source_id = fields.Many2one("security.alert.source", string="Source")
    rule_type = fields.Selection(
        [
            ("cvss_min", "Minimum CVSS Score"),
            ("product_include", "Product Match (Include)"),
            ("product_exclude", "Product Match (Exclude)"),
            ("keyword", "Keyword Filter"),
        ],
        string="Rule Type",
        required=True,
    )
    value = fields.Char(
        string="Value",
        required=True,
        help="CVSS threshold (e.g. 7.0), product name, or keyword",
    )
    action = fields.Selection(
        [
            ("notify", "Send Notification"),
            ("create_action", "Create Action"),
            ("ignore", "Ignore"),
        ],
        string="Action",
        default="notify",
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
