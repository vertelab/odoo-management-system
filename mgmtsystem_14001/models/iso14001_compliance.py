# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Iso14001Compliance(models.Model):
    _name = "iso14001.compliance"
    _description = "Compliance Obligation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "deadline, name"

    name = fields.Char(required=True, translate=True)
    requirement_text = fields.Text(string="Requirement", required=True)
    source = fields.Selection(
        [
            ("law", "Legal Requirement"),
            ("regulation", "Regulation"),
            ("permit", "Permit / License"),
            ("contract", "Contractual"),
            ("voluntary", "Voluntary Commitment"),
            ("other", "Other"),
        ],
        string="Source",
        default="law",
    )
    reference = fields.Char(string="Reference", help="E.g. law number, permit ID")
    deadline = fields.Date(string="Compliance Deadline")
    status = fields.Selection(
        [("compliant", "Compliant"), ("non_compliant", "Non-Compliant"),
         ("not_applicable", "Not Applicable"), ("to_evaluate", "To Evaluate")],
        default="to_evaluate", tracking=True
    )
    responsible_id = fields.Many2one("res.users", string="Responsible")
    evidence = fields.Html(string="Evidence of Compliance")
    iso14001_clause_ids = fields.Many2many(
        "iso14001.clause", string="ISO 14001 Clauses",
        help="Linked to ISO 14001:2026, typically 6.1.3"
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )

    def action_mark_compliant(self):
        self.write({"status": "compliant"})

    def action_mark_noncompliant(self):
        self.write({"status": "non_compliant"})
