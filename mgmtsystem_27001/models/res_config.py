# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    iso27001_scope = fields.Text(
        string="ISMS Scope",
        config_parameter="iso27001.scope",
        help="Scope of the Information Security Management System",
    )
    iso27001_certification_date = fields.Date(
        string="Certification Date",
        config_parameter="iso27001.certification_date",
    )
    iso27001_recertification_date = fields.Date(
        string="Recertification Date",
        config_parameter="iso27001.recertification_date",
    )
    iso27001_risk_acceptance_criteria = fields.Text(
        string="Risk Acceptance Criteria",
        config_parameter="iso27001.risk_acceptance_criteria",
    )
