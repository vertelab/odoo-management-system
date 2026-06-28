# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemReview(models.Model):
    _inherit = "mgmtsystem.review"

    iso_clause_ids = fields.Many2many(
        "sam.iso_clause",
        string="ISO 45001 Klausuler",
        domain="[('clause_number', '=', '9.3')]",
        help="Kopplas till ISO 45001 klausul 9.3: Ledningens genomgång",
    )
    year = fields.Integer(
        string="År",
        default=lambda self: fields.Date.today().year,
    )
    policy_compliance = fields.Html(
        string="Policyuppfyllnad",
        help="Hur väl har arbetsmiljöpolicyn följts?",
    )
    incident_statistics = fields.Integer(
        string="Antal incidenter",
        compute="_compute_incident_statistics",
        store=True,
        help="Antal nonconformities under året",
    )
    training_summary = fields.Html(
        string="Utbildningssammanställning",
        help="Genomförda och planerade utbildningsinsatser",
    )
    improvement_areas = fields.Html(
        string="Förbättringsområden",
        help="Identifierade områden för förbättring",
    )
    next_year_objectives = fields.Html(
        string="Mål för nästa år",
        help="Arbetsmiljömål för kommande år",
    )

    @api.depends("year", "system_id")
    def _compute_incident_statistics(self):
        for rec in self:
            if rec.year:
                start_date = f"{rec.year}-01-01"
                end_date = f"{rec.year}-12-31"
                rec.incident_statistics = self.env[
                    "mgmtsystem.nonconformity"
                ].search_count(
                    [
                        ("create_date", ">=", start_date),
                        ("create_date", "<=", end_date),
                    ]
                )
            else:
                rec.incident_statistics = 0
