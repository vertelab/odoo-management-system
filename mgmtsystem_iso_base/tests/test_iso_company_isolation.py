# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestIsoCompanyIsolation(TransactionCase):
    """Task 2.5 — company isolation on all four core models."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env["res.company"].create({"name": "Bolag A"})
        cls.company_b = cls.env["res.company"].create({"name": "Bolag B"})
        cls.user_a = cls.env["res.users"].create({
            "name": "Användare A",
            "login": "iso_user_a",
            "company_id": cls.company_a.id,
            "company_ids": [(6, 0, [cls.company_a.id])],
            "groups_id": [(6, 0, [
                cls.env.ref("base.group_user").id,
                cls.env.ref("mgmtsystem_iso_base.group_iso_base_manager").id,
            ])],
        })

    def _make_standard(self, company, code):
        return self.env["mgmtsystem.iso.standard"].create({
            "code": code,
            "name": f"Standard {code}",
            "company_id": company.id,
        })

    def test_clauses_isolated_by_company(self):
        """A user only sees clauses of their own company."""
        clause_a = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5.2",
            "name": "A",
            "standard_id": self._make_standard(self.company_a, "TEST-A").id,
            "company_id": self.company_a.id,
        })
        clause_b = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5.2",
            "name": "B",
            "standard_id": self._make_standard(self.company_b, "TEST-B").id,
            "company_id": self.company_b.id,
        })
        visible = self.env["mgmtsystem.iso.clause"].with_user(
            self.user_a
        ).search([])
        self.assertIn(clause_a, visible)
        self.assertNotIn(clause_b, visible)

    def test_gaps_isolated_by_company(self):
        """A user only sees gap analyses of their own company."""
        gap_a = self.env["mgmtsystem.iso.gap"].create({
            "name": "Gap A",
            "standard_id": self._make_standard(self.company_a, "TEST-A").id,
            "company_id": self.company_a.id,
        })
        gap_b = self.env["mgmtsystem.iso.gap"].create({
            "name": "Gap B",
            "standard_id": self._make_standard(self.company_b, "TEST-B").id,
            "company_id": self.company_b.id,
        })
        visible = self.env["mgmtsystem.iso.gap"].with_user(
            self.user_a
        ).search([])
        self.assertIn(gap_a, visible)
        self.assertNotIn(gap_b, visible)
