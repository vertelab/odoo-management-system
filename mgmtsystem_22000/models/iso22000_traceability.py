# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Iso22000Traceability(models.Model):
    _name = "iso22000.traceability"
    _description = "Traceability Test"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "test_date desc"

    name = fields.Char(required=True, translate=True)
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
    )
    batch_id = fields.Char(
        string="Batch/Lot Number",
        required=True,
    )
    direction = fields.Selection(
        [
            ("forward", "Forward (to customer)"),
            ("backward", "Backward (to supplier)"),
            ("both", "Both Directions"),
        ],
        string="Trace Direction",
        default="both",
    )
    test_date = fields.Date(
        string="Test Date",
        required=True,
        default=fields.Date.context_today,
    )
    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")
    time_to_trace = fields.Float(
        string="Time to Trace (hours)",
        compute="_compute_time_to_trace",
        store=True,
        help="Total time to complete traceability test in hours",
    )
    result = fields.Selection(
        [
            ("success", "Successful — 100% traced"),
            ("partial", "Partial — ≥95% traced"),
            ("failed", "Failed — <95% traced"),
        ],
        string="Result",
        required=True,
    )
    percentage_traced = fields.Float(
        string="Percentage Traced",
        help="Percentage of product successfully traced",
    )
    issues_found = fields.Text(
        string="Issues Found",
        help="Any issues or gaps identified during the test",
    )
    corrective_actions = fields.Text(
        string="Corrective Actions",
    )
    tested_by = fields.Many2one(
        "res.users", string="Tested By"
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    @api.depends("start_time", "end_time")
    def _compute_time_to_trace(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                delta = rec.end_time - rec.start_time
                rec.time_to_trace = delta.total_seconds() / 3600.0
            else:
                rec.time_to_trace = 0.0
