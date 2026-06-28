# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemAudit(models.Model):
    _inherit = "mgmtsystem.audit"

    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', 'in', ['9.1', '9.2'])]",
        help="Kopplas till ISO 45001 klausul 9.1/9.2: Övervakning och intern revision",
    )
    checklist_type = fields.Selection(
        [
            ("workplace", "Arbetsplatsrond"),
            ("fire", "Brandskydd"),
            ("ergonomics", "Ergonomi"),
            ("chemical", "Kemikalier"),
            ("psychosocial", "Psykosocial"),
            ("general", "Allmän skyddsrond"),
        ],
        string="Checklisttyp",
        default="general",
    )
    location = fields.Char(string="Plats")
    department_id = fields.Many2one(
        "hr.department",
        string="Avdelning",
    )
