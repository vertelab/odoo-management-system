# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class QualityAlert(models.Model):
    _name = "quality.alert"
    _inherit = ["quality.alert", "quality.nonconformity.mixin"]

    nonconformity_id = fields.Many2one(
        "mgmtsystem.nonconformity",
        string="Avvikelse",
        readonly=True,
        copy=False,
        help="Avvikelse i ledningssystemet som skapades ur denna alert.",
    )
    nonconformity_count = fields.Integer(
        compute="_compute_nonconformity_count",
        string="# Avvikelser",
    )

    def _compute_nonconformity_count(self):
        for alert in self:
            alert.nonconformity_count = 1 if alert.nonconformity_id else 0

    # ── Mixin hooks ─────────────────────────────────────────

    def _nc_origin_model(self):
        return "quality.alert"

    def _nc_origin_label(self):
        return _("Kvalitetsalert")

    def _nc_name(self):
        self.ensure_one()
        return _("Avvikelse: %(name)s") % {"name": self.name}

    def _nc_description(self):
        self.ensure_one()
        parts = [
            _("Avvikelse skapad ur kvalitetsalert %(name)s.") % {"name": self.name},
        ]
        if self.check_id:
            parts.append(_("Kontroll: %s") % self.check_id.name)
        if self.product_id:
            parts.append(_("Produkt: %s") % self.product_id.display_name)
        if self.lot_id:
            parts.append(_("Parti: %s") % self.lot_id.name)
        if self.description:
            parts.append(_("Beskrivning: %s") % self.description)
        if self.action_corrective:
            parts.append(_("Korrigerande åtgärd: %s") % self.action_corrective)
        return "\n".join(parts)

    def _nc_partner(self):
        self.ensure_one()
        return self.partner_id

    def _nc_company(self):
        self.ensure_one()
        return self.company_id or self.env.company

    def _nc_responsible(self):
        self.ensure_one()
        return self.user_id or self.env.user

    def _nc_products(self):
        self.ensure_one()
        return self.product_id, self.lot_id

    def _nc_existing_nonconformity(self):
        self.ensure_one()
        if self.nonconformity_id:
            return self.nonconformity_id
        return self.env["mgmtsystem.nonconformity"].search([
            ("res_model", "=", "quality.alert"),
            ("res_id", "=", self.id),
        ], limit=1)

    def _nc_set_backlink(self, nonconformity):
        self.ensure_one()
        self.nonconformity_id = nonconformity.id
        # If the alert came from a check, link the check too, so both point
        # at the same nonconformity.
        if self.check_id and not self.check_id.nonconformity_id:
            self.check_id.nonconformity_id = nonconformity.id

    # ── Action ──────────────────────────────────────────────

    def action_create_nonconformity(self):
        self.ensure_one()
        self._nc_assert_company()
        return super().action_create_nonconformity()

    def action_view_nonconformity(self):
        self.ensure_one()
        return self._nc_open_nonconformity(self.nonconformity_id)
