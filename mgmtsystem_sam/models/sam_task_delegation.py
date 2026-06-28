# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SamTaskDelegation(models.Model):
    _name = "sam.task_delegation"
    _description = "Uppgiftsfördelning"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_assigned desc"

    name = fields.Char(required=True, translate=True)
    employee_id = fields.Many2one(
        "hr.employee",
        string="Mottagare",
        required=True,
        help="Den anställde som tilldelas arbetsmiljöuppgiften",
    )
    department_id = fields.Many2one(
        "hr.department",
        string="Avdelning",
        related="employee_id.department_id",
        store=True,
    )
    task_description = fields.Text(
        string="Uppgift",
        required=True,
        help="Beskrivning av arbetsmiljöuppgiften",
    )
    responsibility = fields.Text(
        string="Ansvar",
        help="Vad personen ansvarar för",
    )
    resources_required = fields.Text(
        string="Resurser",
        help="Resurser som behövs för att utföra uppgiften (tid, utbildning, befogenheter)",
    )
    date_assigned = fields.Date(
        string="Tilldelad datum",
        default=fields.Date.context_today,
        required=True,
    )
    date_review = fields.Date(string="Nästa översyn")
    company_id = fields.Many2one(
        "res.company",
        string="Företag",
        default=lambda self: self.env.company,
        required=True,
    )
    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', '=', '5.3')]",
        help="Kopplas till ISO 45001 klausul 5.3: Roller, ansvar och befogenheter",
    )
