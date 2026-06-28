# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SamConsultation(models.Model):
    _name = "sam.consultation"
    _description = "Medverkan / Samråd"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_consultation desc"

    name = fields.Char(required=True, translate=True)
    department_id = fields.Many2one(
        "hr.department",
        string="Avdelning",
        required=True,
    )
    discuss_channel_id = fields.Many2one(
        "discuss.channel",
        string="Discuss-kanal",
        help="Automatiskt skapad discuss-kanal för arbetsmiljödiskussioner",
    )
    topic = fields.Text(
        string="Ämne",
        required=True,
        help="Vad samrådet handlar om",
    )
    participant_ids = fields.Many2many(
        "hr.employee",
        "sam_consultation_participant_rel",
        "consultation_id",
        "employee_id",
        string="Deltagare",
    )
    date_consultation = fields.Date(
        string="Samrådsdatum",
        default=fields.Date.context_today,
        required=True,
    )
    conclusion = fields.Text(
        string="Slutsats",
        help="Vad kom man fram till?",
    )
    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', '=', '5.4')]",
        help="Kopplas till ISO 45001 klausul 5.4: Samråd och medverkan",
    )
