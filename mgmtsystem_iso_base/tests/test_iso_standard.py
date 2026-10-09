# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestIsoStandard(TransactionCase):
    """Task 2.1 — mgmtsystem.iso.standard."""

    def test_standard_created(self):
        """A standard is stored with code, name and version."""
        standard = self.env["mgmtsystem.iso.standard"].create({
            "code": "ISO 50001",
            "name": "Energiledning",
            "version": "2018",
        })
        self.assertEqual(standard.code, "ISO 50001")
        self.assertEqual(standard.name, "Energiledning")
        self.assertEqual(standard.version, "2018")
        self.assertTrue(standard.active)

    def test_display_name_includes_version(self):
        standard = self.env["mgmtsystem.iso.standard"].create({
            "code": "ISO 50001",
            "name": "Energiledning",
            "version": "2018",
        })
        self.assertEqual(standard.display_name, "ISO 50001 – Energiledning (2018)")

    @mute_logger("odoo.sql_db")
    def test_duplicate_code_rejected(self):
        """Two standards with the same code are rejected."""
        self.env["mgmtsystem.iso.standard"].create({
            "code": "ISO 50001",
            "name": "Energiledning",
        })
        with self.assertRaises(IntegrityError):
            with self.cr.savepoint():
                self.env["mgmtsystem.iso.standard"].create({
                    "code": "ISO 50001",
                    "name": "Annat namn",
                })

    def test_inactive_standard_hidden_from_selection(self):
        """An inactive standard is not returned when searching active ones."""
        active = self.env["mgmtsystem.iso.standard"].create({
            "code": "ISO 50001",
            "name": "Energiledning",
        })
        inactive = self.env["mgmtsystem.iso.standard"].create({
            "code": "ISO 50002",
            "name": "Arkiverad",
            "active": False,
        })
        found = self.env["mgmtsystem.iso.standard"].search([])
        self.assertIn(active, found)
        self.assertNotIn(inactive, found)
        # Existing clauses for the standard are untouched.
        self.assertTrue(inactive.exists())
