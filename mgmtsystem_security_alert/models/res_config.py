# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_mgmtsystem_security_alert = fields.Boolean(
        string="Säkerhetsbevakning — CERT-SE, CVE, NCSC, Ubuntu USN"
    )
    security_alert_nvd_api_key = fields.Char(
        string="NVD API-nyckel",
        config_parameter="security_alert.nvd_api_key",
    )
    security_alert_cvss_threshold = fields.Float(
        string="Lägsta CVSS-nivå för notifiering",
        default=7.0,
        config_parameter="security_alert.cvss_threshold",
    )
