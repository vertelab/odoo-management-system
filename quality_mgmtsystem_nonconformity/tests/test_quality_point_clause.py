# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Task 5.3 — quality point linked to ISO clauses."""

from odoo.tests.common import TransactionCase


class TestQualityPointClause(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.standard = cls.env.ref("mgmtsystem_iso_base.iso_standard_9001")
        cls.clause = cls.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.8.6",
            "name": "Frigivning av produkter",
            "standard_id": cls.standard.id,
        })
        cls.team = cls.env["quality.alert.team"].create({"name": "Testteam"})
        cls.test_type = cls.env["quality.point.test_type"].search([], limit=1)
        if not cls.test_type:
            cls.test_type = cls.env["quality.point.test_type"].create({
                "name": "Pass/Fail",
                "technical_name": "passfail",
            })

    def _make_point(self, **kwargs):
        vals = {
            "name": "QP-TEST-1",
            "team_id": self.team.id,
            "test_type_id": self.test_type.id,
            "picking_type_ids": [(6, 0, [])],
        }
        vals.update(kwargs)
        return self.env["quality.point"].create(vals)

    def test_point_links_to_clause(self):
        """Task 5.3 — a quality point stores its ISO clause link."""
        point = self._make_point(iso_clause_ids=[(6, 0, self.clause.ids)])
        self.assertEqual(point.iso_clause_ids, self.clause)

    def test_point_without_clause_works(self):
        """A point without a clause link still works."""
        point = self._make_point()
        self.assertFalse(point.iso_clause_ids)

    def test_clause_sees_its_points(self):
        """The clause can be searched from the point side."""
        point = self._make_point(iso_clause_ids=[(6, 0, self.clause.ids)])
        points = self.env["quality.point"].search([
            ("iso_clause_ids", "in", self.clause.id),
        ])
        self.assertIn(point, points)
