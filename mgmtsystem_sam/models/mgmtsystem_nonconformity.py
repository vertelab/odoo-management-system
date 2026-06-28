# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', 'in', ['10.2', '10.3'])]",
        help="Kopplas till ISO 45001 klausul 10.2: Händelse, avvikelse och korrigerande åtgärder",
    )
    incident_type = fields.Selection(
        [
            ("near_miss", "Tillbud"),
            ("accident", "Olycka"),
            ("risk_observation", "Riskobservation"),
            ("road_accident", "Färdolycka"),
        ],
        string="Typ av händelse",
        default="near_miss",
    )
    reported_by_employee_id = fields.Many2one(
        "hr.employee",
        string="Rapporterad av",
        help="Den anställde som rapporterade händelsen",
    )
