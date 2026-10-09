# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class QualityCheck(models.Model):
    _name = "quality.check"
    _inherit = ["quality.check", "quality.nonconformity.mixin"]

    nonconformity_id = fields.Many2one(
        "mgmtsystem.nonconformity",
        string="Avvikelse",
        readonly=True,
        copy=False,
        help="Avvikelse i ledningssystemet som skapades ur denna kontroll.",
    )
    nonconformity_count = fields.Integer(
        compute="_compute_nonconformity_count",
        string="# Avvikelser",
    )

    def _compute_nonconformity_count(self):
        for check in self:
            check.nonconformity_count = 1 if check.nonconformity_id else 0

    # ── Mixin hooks ─────────────────────────────────────────

    def _nc_origin_model(self):
        return "quality.check"

    def _nc_origin_label(self):
        return _("Kvalitetskontroll")

    def _nc_name(self):
        self.ensure_one()
        title = self.title or self.name
        return _("Avvikelse: %(title)s (%(ref)s)") % {
            "title": title,
            "ref": self.name,
        }

    def _nc_description(self):
        self.ensure_one()
        parts = [
            _("Avvikelse skapad ur kvalitetskontroll %(ref)s.") % {"ref": self.name},
        ]
        if self.title:
            parts.append(_("Kontroll: %s") % self.title)
        if self.point_id:
            parts.append(_("Kontrollpunkt: %s") % self.point_id.name)
        if self.quality_state:
            parts.append(
                _("Utfall: %s") % dict(self._fields["quality_state"].selection).get(
                    self.quality_state, self.quality_state
                )
            )
        if self.note:
            parts.append(_("Notering: %s") % self.note)
        if self.additional_note:
            parts.append(_("Ytterligare notering: %s") % self.additional_note)
        return "\n".join(parts)

    def _nc_partner(self):
        self.ensure_one()
        return self.partner_id or self.picking_id.partner_id

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
        # Fallback: a nonconformity created before the back-link was stored.
        return self.env["mgmtsystem.nonconformity"].search([
            ("res_model", "=", "quality.check"),
            ("res_id", "=", self.id),
        ], limit=1)

    def _nc_set_backlink(self, nonconformity):
        self.ensure_one()
        self.nonconformity_id = nonconformity.id

    # ── Action ──────────────────────────────────────────────

    def action_create_nonconformity(self):
        """Create a nonconformity from this check.

        Only offered for a failed check (see the button's invisible
        expression); the guard below makes the rule explicit.
        """
        self.ensure_one()
        self._nc_assert_company()
        return super().action_create_nonconformity()

    def action_view_nonconformity(self):
        """Open the nonconformity created from this check."""
        self.ensure_one()
        return self._nc_open_nonconformity(self.nonconformity_id)
