# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Shared logic for creating a nonconformity out of a quality record.

``quality.check`` and ``quality.alert`` both need to turn a failed quality
event into a ``mgmtsystem.nonconformity``. The derivation rules are the same
for both, so they live here as an abstract mixin.

``mgmtsystem.nonconformity`` has five ``required=True`` fields, four of them
without a default (see design.md Beslut 6). Every one of them must be set, or
``create()`` fails on a NotNullViolation. This mixin derives them all.
"""

from odoo import _, models
from odoo.exceptions import UserError

# Stable key for the reusable origin record created in
# data/nonconformity_origin_data.xml. Looked up by ref_code, not by name,
# because the name is translatable.
ORIGIN_REF_CODE = "quality_check"


class QualityNonconformityMixin(models.AbstractModel):
    """Derive and create a nonconformity from a quality record."""

    _name = "quality.nonconformity.mixin"
    _description = "Quality to Nonconformity Bridge Mixin"

    # ── Hooks the concrete models override ──────────────────

    def _nc_origin_model(self):
        """Model name the nonconformity should point back to."""
        raise NotImplementedError

    def _nc_origin_label(self):
        """Human label for the origin record, used in the description."""
        raise NotImplementedError

    def _nc_name(self):
        """Name for the created nonconformity."""
        raise NotImplementedError

    def _nc_description(self):
        """Description for the created nonconformity."""
        raise NotImplementedError

    def _nc_partner(self):
        """Partner to attach, or an empty recordset."""
        return self.env["res.partner"]

    def _nc_company(self):
        """Company the nonconformity belongs to."""
        return self.env.company

    def _nc_responsible(self):
        """User responsible for the nonconformity."""
        return self.env.user

    def _nc_products(self):
        """(product, lot) tuple, either may be empty."""
        return self.env["product.product"], self.env["stock.lot"]

    # ── Derivation helpers ──────────────────────────────────

    def _nc_derive_partner(self):
        """Partner in order of preference, ending at the company partner.

        A quality check in production often has no external partner. The
        deviation is real even without a customer, so we never block on it.
        """
        self.ensure_one()
        partner = self._nc_partner()
        if partner:
            return partner
        company = self._nc_company()
        if company.partner_id:
            return company.partner_id
        return self.env.user.partner_id

    def _nc_derive_manager(self, responsible):
        """Manager from the responsible user's hr.employee record.

        Chain: res.users -> hr.employee.user_id -> hr.employee.parent_id
        (the field is labelled "Manager") -> parent_id.user_id. Falls back to
        the responsible user when any link is missing.

        The lookup is defensive: `hr` is a declared dependency, but if the
        model is unavailable (module removed, unusual deployment) the manager
        simply falls back instead of raising.
        """
        if "hr.employee" not in self.env:
            return responsible
        employee = self.env["hr.employee"].search(
            [("user_id", "=", responsible.id)], limit=1
        )
        if employee and employee.parent_id and employee.parent_id.user_id:
            return employee.parent_id.user_id
        return responsible

    def _nc_derive_origin(self):
        """The reusable origin record, created by data if missing."""
        origin = self.env["mgmtsystem.nonconformity.origin"].search(
            [("ref_code", "=", ORIGIN_REF_CODE)], limit=1
        )
        if not origin:
            origin = self.env["mgmtsystem.nonconformity.origin"].create({
                "name": _("Kvalitetskontroll"),
                "ref_code": ORIGIN_REF_CODE,
            })
        return origin

    # ── The shared action ───────────────────────────────────

    def _nc_existing_nonconformity(self):
        """The nonconformity already linked to this record, if any."""
        self.ensure_one()
        raise NotImplementedError

    def _nc_set_backlink(self, nonconformity):
        """Store the created nonconformity on this record."""
        self.ensure_one()
        raise NotImplementedError

    def action_create_nonconformity(self):
        """Create (or open) the nonconformity for this quality record.

        Idempotent: a record that already has a nonconformity opens the
        existing one instead of creating a second.
        """
        self.ensure_one()

        existing = self._nc_existing_nonconformity()
        if existing:
            return self._nc_open_nonconformity(existing)

        responsible = self._nc_responsible()
        manager = self._nc_derive_manager(responsible)
        partner = self._nc_derive_partner()
        origin = self._nc_derive_origin()
        company = self._nc_company()
        product, lot = self._nc_products()

        vals = {
            "name": self._nc_name(),
            "description": self._nc_description(),
            "partner_id": partner.id,
            "responsible_user_id": responsible.id,
            "manager_user_id": manager.id,
            "origin_ids": [(6, 0, origin.ids)],
            "company_id": company.id,
            # Generic back-link, already present on the OCA model.
            "res_model": self._nc_origin_model(),
            "res_id": self.id,
        }
        if product:
            vals["reference"] = product.display_name
        nonconformity = self.env["mgmtsystem.nonconformity"].create(vals)
        self._nc_set_backlink(nonconformity)
        return self._nc_open_nonconformity(nonconformity)

    def _nc_open_nonconformity(self, nonconformity):
        """Return an action opening the nonconformity form."""
        return {
            "type": "ir.actions.act_window",
            "name": _("Avvikelse"),
            "res_model": "mgmtsystem.nonconformity",
            "res_id": nonconformity.id,
            "view_mode": "form",
            "target": "current",
        }

    def _nc_assert_company(self):
        """Refuse to bridge a record outside the user's allowed companies."""
        self.ensure_one()
        if self.company_id and self.company_id not in self.env.companies:
            raise UserError(
                _("Du kan inte skapa en avvikelse ur en post i ett annat företag.")
            )
