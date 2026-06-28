# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_mgmtsystem_22000 = fields.Boolean(string="ISO 22000:2018 — Livsmedelssäkerhet (FSMS)")
