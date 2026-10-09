# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Tasks 3.1-3.5 — create a nonconformity from a failed quality check."""

from odoo.tests.common import TransactionCase


class TestQualityCheckBridge(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.team = cls.env["quality.alert.team"].create({"name": "Testteam"})
        cls.test_type = cls.env["quality.point.test_type"].search([], limit=1)
        if not cls.test_type:
            cls.test_type = cls.env["quality.point.test_type"].create({
                "name": "Pass/Fail",
                "technical_name": "passfail",
            })

    def _make_check(self, state="fail", **kwargs):
        vals = {
            "name": "QC-TEST-1",
            "team_id": self.team.id,
            "test_type_id": self.test_type.id,
            "quality_state": state,
            "title": "Kontroll av ytfinish",
        }
        vals.update(kwargs)
        return self.env["quality.check"].create(vals)

    def test_create_nonconformity_from_failed_check(self):
        """Task 3.1 — a nonconformity is created with the derived fields."""
        check = self._make_check(note="Repor i ytan")
        action = check.action_create_nonconformity()

        nc = self.env["mgmtsystem.nonconformity"].browse(action["res_id"])
        self.assertTrue(nc.exists())
        self.assertIn("QC-TEST-1", nc.name)
        self.assertIn("Repor i ytan", nc.description)
        # Required fields all set (design Beslut 6).
        self.assertTrue(nc.partner_id)
        self.assertTrue(nc.responsible_user_id)
        self.assertTrue(nc.manager_user_id)
        self.assertTrue(nc.origin_ids)
        self.assertEqual(nc.company_id, check.company_id)

    def test_backlink_both_ways(self):
        """Tasks 3.2 and 3.3 — res_model/res_id and the check's back-link."""
        check = self._make_check()
        action = check.action_create_nonconformity()
        nc = self.env["mgmtsystem.nonconformity"].browse(action["res_id"])

        self.assertEqual(nc.res_model, "quality.check")
        self.assertEqual(nc.res_id, check.id)
        self.assertEqual(check.nonconformity_id, nc)
        # The origin is the reusable quality_check origin.
        self.assertEqual(nc.origin_ids.ref_code, "quality_check")

    def test_action_opens_nonconformity(self):
        """Task 3.3 — the returned action opens the created record."""
        check = self._make_check()
        action = check.action_create_nonconformity()
        self.assertEqual(action["res_model"], "mgmtsystem.nonconformity")
        self.assertEqual(action["res_id"], check.nonconformity_id.id)
        self.assertEqual(action["view_mode"], "form")

    def test_idempotent(self):
        """Task 3.4 — calling twice yields exactly one nonconformity."""
        check = self._make_check()
        check.action_create_nonconformity()
        first = check.nonconformity_id
        check.action_create_nonconformity()
        self.assertEqual(check.nonconformity_id, first)
        count = self.env["mgmtsystem.nonconformity"].search_count([
            ("res_model", "=", "quality.check"),
            ("res_id", "=", check.id),
        ])
        self.assertEqual(count, 1)

    def test_origin_resolves_in_nonconformity(self):
        """Task 5.2 — the nonconformity resolves its quality origin."""
        check = self._make_check()
        check.action_create_nonconformity()
        nc = check.nonconformity_id
        self.assertEqual(nc.quality_check_id, check)
        self.assertFalse(nc.quality_alert_id)
        action = nc.action_open_quality_origin()
        self.assertEqual(action["res_id"], check.id)

    def test_manager_derived_from_employee(self):
        """Task 3.1 — manager comes from the employee's hr.employee manager."""
        manager_user = self.env["res.users"].create({
            "name": "Chef Testsson",
            "login": "chef_testsson",
        })
        worker_user = self.env["res.users"].create({
            "name": "Arbetare Testsson",
            "login": "arbetare_testsson",
        })
        manager_emp = self.env["hr.employee"].create({
            "name": "Chef Testsson",
            "user_id": manager_user.id,
        })
        self.env["hr.employee"].create({
            "name": "Arbetare Testsson",
            "user_id": worker_user.id,
            "parent_id": manager_emp.id,
        })
        check = self._make_check(user_id=worker_user.id)
        check.action_create_nonconformity()
        nc = check.nonconformity_id
        self.assertEqual(nc.responsible_user_id, worker_user)
        self.assertEqual(nc.manager_user_id, manager_user)

    def test_manager_falls_back_without_employee(self):
        """Task 3.1 — no employee record falls back to the responsible user."""
        user = self.env["res.users"].create({
            "name": "Utan Anställd",
            "login": "utan_anstalld",
        })
        check = self._make_check(user_id=user.id)
        check.action_create_nonconformity()
        nc = check.nonconformity_id
        self.assertEqual(nc.responsible_user_id, user)
        self.assertEqual(nc.manager_user_id, user)

    def test_partner_falls_back_to_company(self):
        """Task 3.1 — a check without a partner still creates the record."""
        check = self._make_check()
        self.assertFalse(check.partner_id)
        check.action_create_nonconformity()
        nc = check.nonconformity_id
        self.assertTrue(nc.partner_id)
        self.assertEqual(nc.partner_id, check.company_id.partner_id)
