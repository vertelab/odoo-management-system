# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Task 6.1 — company isolation on the bridge."""

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestCompanyIsolation(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env["res.company"].create({"name": "Bolag A"})
        cls.company_b = cls.env["res.company"].create({"name": "Bolag B"})
        cls.user_a = cls.env["res.users"].create({
            "name": "Användare A",
            "login": "qnc_user_a",
            "company_id": cls.company_a.id,
            "company_ids": [(6, 0, [cls.company_a.id])],
            "groups_id": [(6, 0, [
                cls.env.ref("base.group_user").id,
                cls.env.ref("quality_ce.group_quality_manager").id,
                cls.env.ref("mgmtsystem.group_mgmtsystem_manager").id,
                cls.env.ref("mgmtsystem_iso_base.group_iso_base_manager").id,
            ])],
        })
        cls.team_b = cls.env["quality.alert.team"].create({
            "name": "Team B",
            "company_id": cls.company_b.id,
        })
        cls.test_type = cls.env["quality.point.test_type"].search([], limit=1)
        if not cls.test_type:
            cls.test_type = cls.env["quality.point.test_type"].create({
                "name": "Pass/Fail",
                "technical_name": "passfail",
            })

    def test_cannot_bridge_check_from_another_company(self):
        """Task 6.1 — a check in another company is refused."""
        check = self.env["quality.check"].create({
            "name": "QC-B-1",
            "team_id": self.team_b.id,
            "test_type_id": self.test_type.id,
            "quality_state": "fail",
            "company_id": self.company_b.id,
        })
        with self.assertRaises(UserError):
            check.with_user(self.user_a).action_create_nonconformity()

    def test_clause_from_another_company_not_offered(self):
        """Task 6.1 — clauses are company-isolated in the selection."""
        other_standard = self.env["mgmtsystem.iso.standard"].create({
            "code": "TEST-B",
            "name": "Bolag B standard",
            "company_id": self.company_b.id,
        })
        clause_b = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.1",
            "name": "Bolag B klausul",
            "standard_id": other_standard.id,
            "company_id": self.company_b.id,
        })
        visible = self.env["mgmtsystem.iso.clause"].with_user(
            self.user_a
        ).search([])
        self.assertNotIn(clause_b, visible)
