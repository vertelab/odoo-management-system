# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso42001SoaLine(models.Model):
    _name = "iso42001.soa.line"
    _description = "SoA Line"
    _order = "control_id"

    soa_id = fields.Many2one("iso42001.soa", required=True, ondelete="cascade")
    control_id = fields.Many2one(
        "iso42001.control", string="Annex A Control", required=True
    )
    company_id = fields.Many2one(related="soa_id.company_id", store=True)
    applicable = fields.Boolean(string="Applicable", default=True)
    implemented = fields.Boolean(string="Implemented")
    justification = fields.Text(string="Justification")
    implementation_status = fields.Text(string="Implementation Status")
