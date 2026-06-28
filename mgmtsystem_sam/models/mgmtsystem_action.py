# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', 'in', ['6.2', '8.1'])]",
        help="Kopplas till ISO 45001 klausul 6.2 och 8.1: Mål och verksamhetsstyrning",
    )
    hazard_id = fields.Many2one(
        "mgmtsystem.hazard",
        string="Hazard",
        help="Länk till riskbedömningen som åtgärden härrör från",
    )
    verification_result = fields.Text(
        string="Verifieringsresultat",
        help="Resultat av kontroll/uppföljning av åtgärden",
    )
