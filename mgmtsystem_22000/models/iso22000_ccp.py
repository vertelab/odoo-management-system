# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso22000Ccp(models.Model):
    _name = "iso22000.ccp"
    _description = "Critical Control Point (CCP)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    haccp_id = fields.Many2one(
        "iso22000.haccp",
        string="HACCP Plan",
        required=True,
        ondelete="cascade",
    )
    hazard_id = fields.Many2one(
        "iso22000.hazard",
        string="Hazard",
        help="The hazard this CCP controls",
    )
    critical_limit = fields.Char(
        string="Critical Limit",
        required=True,
        help="Measurable limit, e.g. '< 4°C', '> 72°C for 15 seconds'",
    )
    monitoring_method = fields.Text(
        string="Monitoring Method",
        help="What to monitor, how, when, and by whom",
    )
    frequency = fields.Selection(
        [
            ("continuous", "Continuous"),
            ("per_batch", "Per Batch"),
            ("hourly", "Hourly"),
            ("per_shift", "Per Shift"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
        ],
        string="Monitoring Frequency",
        default="per_batch",
    )
    corrective_action = fields.Text(
        string="Corrective Action",
        help="Action to take when critical limit is exceeded",
    )
    responsible_id = fields.Many2one(
        "res.users", string="Responsible Person"
    )
    verification_method = fields.Text(
        string="Verification Method",
        help="How to verify the CCP is working effectively",
    )
    records_kept = fields.Char(
        string="Records",
        help="What records are kept for this CCP",
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
