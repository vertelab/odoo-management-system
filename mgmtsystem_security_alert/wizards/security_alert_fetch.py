# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SecurityAlertFetchWizard(models.TransientModel):
    _name = "security.alert.fetch.wizard"
    _description = "Manual Security Alert Fetch"

    def action_fetch_all(self):
        """Fetch from all active sources."""
        sources = self.env["security.alert.source"].search([("active", "=", True)])
        count = 0
        for source in sources:
            source.fetch_alerts()
            count += 1
        return {
            "type": "ir.actions.act_window_close",
            "info": f"Fetched from {count} sources",
        }
