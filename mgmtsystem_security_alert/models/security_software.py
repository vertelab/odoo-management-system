# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SecuritySoftware(models.Model):
    _name = "security.software"
    _description = "Software Inventory for CVE Tracking"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name, version"
    _rec_name = "display_name"

    name = fields.Char(required=True)
    version = fields.Char(required=True)
    display_name = fields.Char(compute="_compute_display_name", store=True)

    start_date = fields.Date(string="Used Since")
    end_date = fields.Date(string="Used Until", help="Leave empty if still in use")
    active = fields.Boolean(default=True)

    usage_description = fields.Text(
        string="Usage Description",
        help="Describe how/where this software is used in the organization",
    )

    parent_id = fields.Many2one(
        "security.software",
        string="Part Of",
        help="E.g. 'PostgreSQL 16' is part of the 'Odoo 18' stack",
        index=True,
    )
    child_ids = fields.One2many("security.software", "parent_id", string="Dependencies")
    dependency_ids = fields.Many2many(
        "security.software",
        "security_software_dependency_rel",
        "software_id",
        "dependency_id",
        string="Depends On",
    )

    vendor = fields.Char(string="Vendor")
    cpe_name = fields.Char(
        string="CPE Name",
        help="Common Platform Enumeration, e.g. 'cpe:2.3:o:canonical:ubuntu_linux:24.04'",
    )
    icon = fields.Binary(string="Icon")
    icon_filename = fields.Char()

    software_type = fields.Selection(
        [
            ("os", "Operating System"),
            ("application", "Application"),
            ("database", "Database"),
            ("webserver", "Web Server"),
            ("framework", "Framework"),
            ("library", "Library"),
            ("middleware", "Middleware"),
            ("other", "Other"),
        ],
        string="Type",
        default="application",
    )

    alert_ids = fields.One2many(
        "security.alert",
        "software_id",
        string="Related Alerts",
    )
    alert_count = fields.Integer(
        compute="_compute_alert_count",
        string="Alert Count",
    )

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    _sql_constraints = [
        (
            "name_version_uniq",
            "unique(name, version, company_id)",
            "Software with this name and version already exists for this company!",
        ),
    ]

    @api.depends("name", "version")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} {rec.version}"

    def _compute_alert_count(self):
        for sw in self:
            sw.alert_count = self.env["security.alert"].search_count([
                ("software_id", "=", sw.id),
            ])

    def kanban_image(self):
        """Return icon for kanban view. Defaults to fa-cube."""
        return self.icon or None
