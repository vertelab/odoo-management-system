# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SecurityAlert(models.Model):
    _name = "security.alert"
    _description = "Security Alert"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "published_date desc, cvss_score desc"
    _rec_name = "name"

    name = fields.Char(required=True)
    source_id = fields.Many2one(
        "security.alert.source",
        string="Source",
        required=True,
        index=True,
    )
    source_ref = fields.Char(
        string="Source Reference",
        index=True,
        help="CVE-ID, USN-ID, URL, or other unique source reference",
    )
    description = fields.Html(string="Description")
    severity = fields.Selection(
        [
            ("critical", "Critical"),
            ("high", "High"),
            ("medium", "Medium"),
            ("low", "Low"),
            ("info", "Info"),
        ],
        string="Severity",
        default="info",
    )
    cvss_score = fields.Float(string="CVSS Score", digits=(3, 1))
    cvss_vector = fields.Char(string="CVSS Vector")
    published_date = fields.Date(string="Published")
    affected_products = fields.Text(string="Affected Products")
    mitigation = fields.Html(string="Mitigation")
    state = fields.Selection(
        [
            ("new", "New"),
            ("acknowledged", "Acknowledged"),
            ("in_progress", "In Progress"),
            ("resolved", "Resolved"),
            ("false_positive", "False Positive"),
            ("dismissed", "Dismissed"),
        ],
        default="new",
        tracking=True,
    )
    assigned_to = fields.Many2one("res.users", string="Assigned To")
    control_ids = fields.Many2many(
        "mgmtsystem.security.control",
        string="ISO 27001 Controls",
        help="Linked Annex A controls",
    )
    security_event_id = fields.Many2one(
        "mgmtsystem.security.event",
        string="Security Event",
        help="Linked EBIOS security event",
    )
    action_ids = fields.One2many(
        "security.alert.action",
        "alert_id",
        string="Actions",
    )

    # Software inventory linking
    software_id = fields.Many2one(
        "security.software",
        string="Related Software",
        index=True,
    )
    matched_software = fields.Boolean(
        string="Matched Software",
        default=False,
        help="This alert matches software in our inventory",
    )

    # AI assessment fields
    ai_relevance_score = fields.Float(
        string="AI Relevance (0-1)",
        digits=(3, 2),
        help="AI-assessed relevance for the organization",
    )
    ai_risk_assessment = fields.Text(string="AI Risk Assessment")
    ai_mitigation_suggestion = fields.Text(string="AI Mitigation Suggestion")
    ai_assessed_date = fields.Datetime(string="AI Assessed Date")

    # Raw data for debugging
    raw_data = fields.Text(string="Raw Data (JSON)")

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    _sql_constraints = [
        (
            "source_ref_uniq_per_source",
            "unique(source_id, source_ref)",
            "Alert already exists for this source and reference!",
        ),
    ]

    def action_acknowledge(self):
        self.write({"state": "acknowledged"})

    def action_start_work(self):
        self.write({"state": "in_progress"})

    def action_resolve(self):
        self.write({"state": "resolved"})

    def action_false_positive(self):
        self.write({"state": "false_positive"})

    def action_dismiss(self):
        self.write({"state": "dismissed"})

    def action_reopen(self):
        self.write({"state": "new"})

    def action_ai_assess_relevance(self):
        """Call AI to assess if this alert is relevant."""
        self.ensure_one()
        coworker = self.env['ai.coworker'].search(
            [('name', '=', 'Security Alert Relevance')], limit=1)
        if not coworker:
            _logger.warning('AI coworker not available for alert assessment')
            return False

        software_context = self._get_software_inventory_context()
        prompt = (
            f"Bedöm om följande säkerhetsvarning är relevant för vår organisation.\n\n"
            f"VARNING:\nTitel: {self.name}\nCVSS: {self.cvss_score}\n"
            f"Beskrivning: {self.description}\n"
            f"Berörda produkter: {self.affected_products}\n\n"
            f"VÅR PROGRAMVARUINVENTERING:\n{software_context}\n\n"
            f"Bedöm relevans på en skala 0-1 och ge en kort riskanalys."
        )
        try:
            result_text = coworker.run(prompt)
            import json as _json
            try:
                result = _json.loads(result_text)
            except Exception:
                result = {'score': 0.5, 'risk_assessment': result_text[:500]}
            self.write({
                "ai_relevance_score": result.get("score", 0.0) if isinstance(result, dict) else 0.5,
                "ai_risk_assessment": result.get("risk_assessment", "") if isinstance(result, dict) else str(result),
                "ai_mitigation_suggestion": result.get("mitigation", "") if isinstance(result, dict) else "",
                "ai_assessed_date": fields.Datetime.now(),
            })
        except Exception as e:
            _logger.warning('AI assessment failed: %s', e)

    def _get_software_inventory_context(self):
        software = self.env["security.software"].search([
            ("company_id", "=", self.env.company.id),
            ("active", "=", True),
        ])
        lines = []
        for sw in software:
            lines.append(f"- {sw.name} {sw.version} ({sw.usage_description or 'ingen beskrivning'})")
        return "\n".join(lines) if lines else "Ingen programvaruinventering registrerad"

    def cron_ai_assess_unassessed(self):
        """Cron: AI-assess new unassessed alerts."""
        alerts = self.search([
            ("state", "=", "new"),
            ("ai_relevance_score", "=", 0.0),
        ], limit=10)
        for alert in alerts:
            try:
                alert.action_ai_assess_relevance()
            except Exception:
                pass
