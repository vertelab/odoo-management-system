# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestIsoGap(TransactionCase):
    """Tasks 2.3 and 2.4 — mgmtsystem.iso.gap and .gap.line."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.standard = cls.env.ref("mgmtsystem_iso_base.iso_standard_9001")
        cls.clause = cls.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.6.2",
            "name": "Kvalitetsmål",
            "standard_id": cls.standard.id,
        })

    def test_gap_created_for_standard(self):
        """A gap analysis is created with its standard."""
        gap = self.env["mgmtsystem.iso.gap"].create({
            "name": "Gap 2026",
            "standard_id": self.standard.id,
        })
        self.assertEqual(gap.standard_id, self.standard)
        self.assertEqual(gap.state, "draft")

    @mute_logger("odoo.sql_db")
    def test_gap_without_standard_rejected(self):
        """A gap analysis without a standard is rejected."""
        with self.assertRaises(IntegrityError):
            with self.cr.savepoint():
                self.env["mgmtsystem.iso.gap"].create({"name": "Utan standard"})

    def test_gap_state_flow(self):
        """The state follows draft -> in_progress -> done."""
        gap = self.env["mgmtsystem.iso.gap"].create({
            "name": "Gap 2026",
            "standard_id": self.standard.id,
        })
        self.assertEqual(gap.state, "draft")
        gap.action_start()
        self.assertEqual(gap.state, "in_progress")
        gap.action_done()
        self.assertEqual(gap.state, "done")
        gap.action_draft()
        self.assertEqual(gap.state, "draft")

    def test_new_line_has_maturity_zero(self):
        """An untouched gap line is maturity level 0."""
        gap = self.env["mgmtsystem.iso.gap"].create({
            "name": "Gap 2026",
            "standard_id": self.standard.id,
        })
        line = self.env["mgmtsystem.iso.gap.line"].create({
            "gap_id": gap.id,
            "clause_id": self.clause.id,
        })
        self.assertEqual(line.maturity_level, "0")
        self.assertEqual(line.status, "open")

    def test_maturity_level_saved(self):
        """A maturity level set on a line is stored."""
        gap = self.env["mgmtsystem.iso.gap"].create({
            "name": "Gap 2026",
            "standard_id": self.standard.id,
        })
        line = self.env["mgmtsystem.iso.gap.line"].create({
            "gap_id": gap.id,
            "clause_id": self.clause.id,
            "maturity_level": "3",
        })
        self.assertEqual(line.maturity_level, "3")

    def test_finding_and_recommendation_saved(self):
        """Finding and recommendation are stored per line, linked to clause."""
        gap = self.env["mgmtsystem.iso.gap"].create({
            "name": "Gap 2026",
            "standard_id": self.standard.id,
        })
        line = self.env["mgmtsystem.iso.gap.line"].create({
            "gap_id": gap.id,
            "clause_id": self.clause.id,
            "finding": "Inga mål dokumenterade",
            "recommendation": "Inför mål med KPI",
        })
        self.assertEqual(line.finding, "Inga mål dokumenterade")
        self.assertEqual(line.recommendation, "Inför mål med KPI")
        self.assertEqual(line.clause_id, self.clause)

    def test_line_inherits_company_from_gap(self):
        """A line's company follows its gap analysis."""
        gap = self.env["mgmtsystem.iso.gap"].create({
            "name": "Gap 2026",
            "standard_id": self.standard.id,
        })
        line = self.env["mgmtsystem.iso.gap.line"].create({
            "gap_id": gap.id,
            "clause_id": self.clause.id,
        })
        self.assertEqual(line.company_id, gap.company_id)
