# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Tasks 4.1 and 4.2 — create a nonconformity from a quality alert."""

from odoo.tests.common import TransactionCase


class TestQualityAlertBridge(TransactionCase):

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

    def _make_check(self, **kwargs):
        vals = {
            "name": "QC-ALERT-1",
            "team_id": self.team.id,
            "test_type_id": self.test_type.id,
            "quality_state": "fail",
        }
        vals.update(kwargs)
        return self.env["quality.check"].create(vals)

    def _make_alert(self, **kwargs):
        vals = {
            "name": "QA-TEST-1",
            "team_id": self.team.id,
            "description": "Kund klagar på leverans",
        }
        vals.update(kwargs)
        return self.env["quality.alert"].create(vals)

    def test_create_nonconformity_from_alert(self):
        """Task 4.1 — a nonconformity is created from an alert."""
        alert = self._make_alert()
        action = alert.action_create_nonconformity()
        nc = self.env["mgmtsystem.nonconformity"].browse(action["res_id"])

        self.assertTrue(nc.exists())
        self.assertIn("QA-TEST-1", nc.name)
        self.assertIn("Kund klagar", nc.description)
        self.assertEqual(nc.res_model, "quality.alert")
        self.assertEqual(nc.res_id, alert.id)
        self.assertEqual(alert.nonconformity_id, nc)
        self.assertTrue(nc.partner_id)
        self.assertTrue(nc.responsible_user_id)
        self.assertTrue(nc.manager_user_id)
        self.assertTrue(nc.origin_ids)

    def test_alert_with_check_links_both(self):
        """Task 4.1 — an alert with a check links the nonconformity to both."""
        check = self._make_check()
        alert = self._make_alert(check_id=check.id)
        alert.action_create_nonconformity()
        nc = alert.nonconformity_id

        self.assertEqual(nc.res_model, "quality.alert")
        self.assertEqual(nc.res_id, alert.id)
        # The check is linked too, so both point at the same nonconformity.
        self.assertEqual(check.nonconformity_id, nc)

    def test_alert_idempotent(self):
        """Task 4.2 — repeated calls yield exactly one nonconformity."""
        alert = self._make_alert()
        alert.action_create_nonconformity()
        first = alert.nonconformity_id
        alert.action_create_nonconformity()
        self.assertEqual(alert.nonconformity_id, first)
        count = self.env["mgmtsystem.nonconformity"].search_count([
            ("res_model", "=", "quality.alert"),
            ("res_id", "=", alert.id),
        ])
        self.assertEqual(count, 1)
