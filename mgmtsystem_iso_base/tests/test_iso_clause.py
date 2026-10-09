# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestIsoClause(TransactionCase):
    """Task 2.2 — mgmtsystem.iso.clause."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Use the standards seeded by data/iso_standard_data.xml so the
        # unique code constraint is not violated.
        cls.standard_9001 = cls.env.ref(
            "mgmtsystem_iso_base.iso_standard_9001"
        )
        cls.standard_27001 = cls.env.ref(
            "mgmtsystem_iso_base.iso_standard_27001"
        )

    def test_clause_created_under_standard(self):
        """A clause is stored under its standard with its number."""
        clause = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5.2",
            "name": "Kvalitetspolicy",
            "standard_id": self.standard_9001.id,
        })
        self.assertEqual(clause.standard_id, self.standard_9001)
        self.assertEqual(clause.clause_number, "T.5.2")

    def test_same_number_in_two_standards_allowed(self):
        """Clause 5.2 may exist in both ISO 9001 and ISO 27001."""
        c1 = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5.2",
            "name": "Kvalitetspolicy",
            "standard_id": self.standard_9001.id,
        })
        c2 = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5.2",
            "name": "Informationssäkerhetspolicy",
            "standard_id": self.standard_27001.id,
        })
        self.assertNotEqual(c1, c2)
        self.assertEqual(c1.standard_id, self.standard_9001)
        self.assertEqual(c2.standard_id, self.standard_27001)

    @mute_logger("odoo.sql_db")
    def test_duplicate_number_in_same_standard_rejected(self):
        """A duplicate clause number within one standard is rejected."""
        self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5.2",
            "name": "Kvalitetspolicy",
            "standard_id": self.standard_9001.id,
        })
        with self.assertRaises(IntegrityError):
            with self.cr.savepoint():
                self.env["mgmtsystem.iso.clause"].create({
                    "clause_number": "T.5.2",
                    "name": "Dubblett",
                    "standard_id": self.standard_9001.id,
                })

    def test_child_clause_links_to_parent(self):
        """A child clause appears in the parent's tree."""
        parent = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5",
            "name": "Ledarskap",
            "standard_id": self.standard_9001.id,
        })
        child = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5.1",
            "name": "Ledarskap och engagemang",
            "standard_id": self.standard_9001.id,
            "parent_id": parent.id,
        })
        self.assertEqual(child.parent_id, parent)
        self.assertIn(child, parent.child_ids)

    def test_parent_must_belong_to_same_standard(self):
        """A parent from another standard is rejected."""
        parent_27001 = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5",
            "name": "Ledarskap",
            "standard_id": self.standard_27001.id,
        })
        with self.assertRaises(ValidationError):
            self.env["mgmtsystem.iso.clause"].create({
                "clause_number": "T.5.1",
                "name": "Fel standard",
                "standard_id": self.standard_9001.id,
                "parent_id": parent_27001.id,
            })

    def test_display_name(self):
        """The display name shows number and name."""
        clause = self.env["mgmtsystem.iso.clause"].create({
            "clause_number": "T.5.2",
            "name": "Kvalitetspolicy",
            "standard_id": self.standard_9001.id,
        })
        self.assertEqual(clause.display_name, "T.5.2 Kvalitetspolicy")
