# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso42001Control(models.Model):
    _name = "iso42001.control"
    _description = "ISO 42001 Annex A Control"
    _order = "control_ref"

    control_ref = fields.Char(
        string="Annex A Ref", required=True,
        help="ISO 42001:2023 Annex A control reference, e.g. 'A.2.1', 'A.7.4'",
        index=True,
    )
    control_area = fields.Selection(
        [
            ("A.2", "A.2 Policies related to AI"),
            ("A.3", "A.3 Internal organization"),
            ("A.4", "A.4 Resources for AI systems"),
            ("A.5", "A.5 Assessing impacts of AI systems"),
            ("A.6", "A.6 AI system life cycle"),
            ("A.7", "A.7 Data for AI systems"),
            ("A.8", "A.8 Information for interested parties"),
            ("A.9", "A.9 Use of AI systems"),
            ("A.10", "A.10 Third-party and customer relationships"),
        ],
        string="Control Area", required=True, index=True,
    )
    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    control_type = fields.Selection(
        [
            ("policy", "Policy / Governance"),
            ("process", "Process"),
            ("technical", "Technical"),
            ("documentation", "Documentation"),
        ],
        string="Control Type", default="process",
    )
    sequence = fields.Integer(default=10)
    iso42001_clause_ids = fields.Many2many(
        "iso42001.clause", "iso42001_control_clause_rel",
        "control_id", "clause_id", string="ISO 42001 Clauses"
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company
    )

    _sql_constraints = [
        ("control_ref_unique", "unique(control_ref)", "Annex A control reference must be unique!"),
    ]
