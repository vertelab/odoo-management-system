# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Task 5.1 and 5.2 — the legacy migration is idempotent and lossless.

These tests create the old ``iso9001_*`` tables by hand (they no longer
exist as models), seed them with rows, run the migration twice, and assert
that every clause and gap analysis lands in the core exactly once.
"""

from odoo.tests.common import TransactionCase

from odoo.addons.mgmtsystem_9001.iso9001_core_migration import (
    migrate_iso9001_to_core,
)


class TestIso9001Migration(TransactionCase):

    def setUp(self):
        super().setUp()
        self.standard = self.env.ref(
            "mgmtsystem_iso_base.iso_standard_9001"
        )
        self._create_legacy_tables()
        self._seed_legacy_rows()

    def _create_legacy_tables(self):
        """Recreate the pre-change tables as they existed before."""
        self.env.cr.execute("""
            CREATE TABLE IF NOT EXISTS iso9001_clause (
                id serial PRIMARY KEY,
                name varchar,
                clause_number varchar,
                description text,
                parent_id integer,
                sequence integer,
                company_id integer
            )
        """)
        self.env.cr.execute("""
            CREATE TABLE IF NOT EXISTS iso9001_gap (
                id serial PRIMARY KEY,
                name varchar,
                date date,
                assessed_by integer,
                state varchar,
                company_id integer,
                notes text
            )
        """)
        self.env.cr.execute("""
            CREATE TABLE IF NOT EXISTS iso9001_gap_line (
                id serial PRIMARY KEY,
                gap_id integer,
                clause_id integer,
                maturity_level varchar,
                finding text,
                recommendation text,
                status varchar
            )
        """)

    def _seed_legacy_rows(self):
        company = self.env.company
        self.env.cr.execute(
            "INSERT INTO iso9001_clause "
            "(name, clause_number, description, parent_id, sequence, company_id) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            ("Ledarskap", "5", "Legacy parent", None, 20, company.id),
        )
        self.legacy_parent_id = self.env.cr.fetchone()[0]
        self.env.cr.execute(
            "INSERT INTO iso9001_clause "
            "(name, clause_number, description, parent_id, sequence, company_id) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            ("Kvalitetspolicy", "5.2", "Legacy child",
             self.legacy_parent_id, 22, company.id),
        )
        self.legacy_child_id = self.env.cr.fetchone()[0]
        self.env.cr.execute(
            "INSERT INTO iso9001_gap "
            "(name, date, assessed_by, state, company_id, notes) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            ("Legacy gap 2025", "2025-06-01", None, "done", company.id, "n"),
        )
        self.legacy_gap_id = self.env.cr.fetchone()[0]
        self.env.cr.execute(
            "INSERT INTO iso9001_gap_line "
            "(gap_id, clause_id, maturity_level, finding, recommendation, status) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (self.legacy_gap_id, self.legacy_child_id, "4",
             "Legacy finding", "Legacy recommendation", "resolved"),
        )

    def _run_migration(self):
        migrate_iso9001_to_core(self.env.cr, None)

    def test_clauses_migrated_to_core(self):
        """Legacy clauses land in the core, linked to ISO 9001."""
        self._run_migration()
        clause = self.env["mgmtsystem.iso.clause"].search([
            ("clause_number", "=", "5.2"),
            ("standard_id", "=", self.standard.id),
        ])
        self.assertEqual(len(clause), 1)
        self.assertEqual(clause.name, "Kvalitetspolicy")
        # Parent link is preserved.
        parent = clause.parent_id
        self.assertTrue(parent)
        self.assertEqual(parent.clause_number, "5")

    def test_gap_and_lines_migrated(self):
        """The legacy gap analysis and its lines land in the core."""
        self._run_migration()
        gap = self.env["mgmtsystem.iso.gap"].search([
            ("name", "=", "Legacy gap 2025"),
            ("standard_id", "=", self.standard.id),
        ])
        self.assertEqual(len(gap), 1)
        self.assertEqual(gap.state, "done")
        self.assertEqual(len(gap.line_ids), 1)
        line = gap.line_ids
        self.assertEqual(line.maturity_level, "4")
        self.assertEqual(line.finding, "Legacy finding")
        self.assertEqual(line.status, "resolved")

    def test_second_run_creates_no_duplicates(self):
        """Running the migration twice does not duplicate anything."""
        self._run_migration()
        clauses_after_first = self.env["mgmtsystem.iso.clause"].search_count([
            ("standard_id", "=", self.standard.id),
        ])
        gaps_after_first = self.env["mgmtsystem.iso.gap"].search_count([
            ("standard_id", "=", self.standard.id),
        ])
        lines_after_first = self.env["mgmtsystem.iso.gap.line"].search_count([
            ("gap_id.standard_id", "=", self.standard.id),
        ])

        self._run_migration()

        self.assertEqual(
            self.env["mgmtsystem.iso.clause"].search_count([
                ("standard_id", "=", self.standard.id),
            ]),
            clauses_after_first,
        )
        self.assertEqual(
            self.env["mgmtsystem.iso.gap"].search_count([
                ("standard_id", "=", self.standard.id),
            ]),
            gaps_after_first,
        )
        self.assertEqual(
            self.env["mgmtsystem.iso.gap.line"].search_count([
                ("gap_id.standard_id", "=", self.standard.id),
            ]),
            lines_after_first,
        )

    def test_no_legacy_tables_is_a_noop(self):
        """The migration is safe when the old tables never existed."""
        self.env.cr.execute("DROP TABLE iso9001_gap_line")
        self.env.cr.execute("DROP TABLE iso9001_gap")
        self.env.cr.execute("DROP TABLE iso9001_clause")
        # Must not raise.
        self._run_migration()
