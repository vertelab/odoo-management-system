# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SamInstruction(models.Model):
    _name = "sam.instruction"
    _description = "Arbets- och skyddsinstruktion"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, translate=True)
    department_id = fields.Many2one(
        "hr.department",
        string="Avdelning",
    )
    task_description = fields.Text(
        string="Arbetsmoment",
        required=True,
    )
    risk_description = fields.Text(
        string="Riskbeskrivning",
        help="Vilka risker finns med arbetsmomentet?",
    )
    safety_measures = fields.Text(
        string="Skyddsåtgärder",
        help="Åtgärder för att förebygga riskerna",
    )
    ppe_required = fields.Text(
        string="Personlig skyddsutrustning",
        help="Vilken skyddsutrustning krävs?",
    )
    emergency_procedure = fields.Text(
        string="Nödprocedur",
        help="Vad görs vid olycka eller nödläge?",
    )
    revision_date = fields.Date(
        string="Revisionsdatum",
        default=fields.Date.context_today,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Företag",
        default=lambda self: self.env.company,
        required=True,
    )
    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', 'in', ['7.2', '8.1'])]",
        help="Kopplas till ISO 45001 klausul 7.2 och 8.1",
    )
