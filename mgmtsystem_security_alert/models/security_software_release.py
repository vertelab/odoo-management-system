# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SecuritySoftwareRelease(models.Model):
    _name = "security.software.release"
    _description = "Ubuntu Release for CVE Tracking"
    _order = "codename"

    name = fields.Char(required=True, help="E.g. 'Ubuntu 24.04 LTS'")
    codename = fields.Char(required=True, help="E.g. 'noble'")
    version = fields.Char(required=True, help="E.g. '24.04'")
    active = fields.Boolean(default=True)
    lts = fields.Boolean(string="LTS", default=True)
