# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SecurityControl(models.Model):
    _inherit = "mgmtsystem.security.control"
    _order = "control_ref"

    control_ref = fields.Char(
        string="Annex A Ref",
        help="ISO 27001:2022 Annex A control reference, e.g. '5.1', '8.11'",
        index=True,
    )
    control_group = fields.Selection(
        [
            ("organizational", "Organisatoriska (5)"),
            ("people", "Personkontroller (6)"),
            ("physical", "Fysiska (7)"),
            ("technological", "Tekniska (8)"),
        ],
        string="Kontrollgrupp",
        help="ISO 27001:2022 Annex A control group",
        index=True,
    )
    control_type = fields.Selection(
        [
            ("preventive", "Förebyggande"),
            ("detective", "Upptäckande"),
            ("corrective", "Korrigerande"),
        ],
        string="Kontrolltyp",
        help="Type of security control",
    )
    iso27001_clause_ids = fields.Many2many(
        "iso27001.clause",
        "iso27001_control_clause_rel",
        "control_id",
        "clause_id",
        string="ISO 27001 Clauses",
        help="ISO 27001:2022 clauses this control relates to",
    )
    sequence = fields.Integer(
        default=10,
        help="Sequence for ordering controls within a group",
    )

    _sql_constraints = [
        (
            "control_ref_unique",
            "unique(control_ref)",
            "Annex A control reference must be unique!",
        ),
    ]
