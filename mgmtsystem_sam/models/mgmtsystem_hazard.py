# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemHazard(models.Model):
    _inherit = "mgmtsystem.hazard"

    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', '=', '6.1')]",
        help="Kopplas till ISO 45001 klausul 6.1: Åtgärder för att hantera risker",
    )
    risk_category = fields.Selection(
        [
            ("physical", "Fysisk"),
            ("psychosocial", "Psykosocial"),
            ("chemical", "Kemisk"),
            ("biological", "Biologisk"),
            ("ergonomic", "Ergonomisk"),
        ],
        string="Riskkategori",
    )
    assessed_by = fields.Many2many(
        "hr.employee",
        "mgmtsystem_hazard_assessed_rel",
        "hazard_id",
        "employee_id",
        string="Bedömd av",
        help="Personer som deltagit i riskbedömningen",
    )
