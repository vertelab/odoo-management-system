# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class MgmtSystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    quality_check_id = fields.Many2one(
        "quality.check",
        string="Ursprunglig kontroll",
        compute="_compute_quality_origin",
        help="Kvalitetskontrollen som avvikelsen skapades ur, om någon.",
    )
    quality_alert_id = fields.Many2one(
        "quality.alert",
        string="Ursprunglig alert",
        compute="_compute_quality_origin",
        help="Kvalitetsalerten som avvikelsen skapades ur, om någon.",
    )

    def _compute_quality_origin(self):
        """Resolve the generic res_model/res_id back-link into a record.

        The OCA model stores the origin generically; these computed fields
        make it usable in the form without changing the OCA model's shape.
        """
        for nc in self:
            nc.quality_check_id = False
            nc.quality_alert_id = False
            if nc.res_model == "quality.check" and nc.res_id:
                nc.quality_check_id = self.env["quality.check"].browse(
                    nc.res_id
                ).exists()
            elif nc.res_model == "quality.alert" and nc.res_id:
                nc.quality_alert_id = self.env["quality.alert"].browse(
                    nc.res_id
                ).exists()

    def action_open_quality_origin(self):
        """Open the quality record this nonconformity came from."""
        self.ensure_one()
        if self.quality_check_id:
            return {
                "type": "ir.actions.act_window",
                "name": _("Kvalitetskontroll"),
                "res_model": "quality.check",
                "res_id": self.quality_check_id.id,
                "view_mode": "form",
                "target": "current",
            }
        if self.quality_alert_id:
            return {
                "type": "ir.actions.act_window",
                "name": _("Kvalitetsalert"),
                "res_model": "quality.alert",
                "res_id": self.quality_alert_id.id,
                "view_mode": "form",
                "target": "current",
            }
        return False
