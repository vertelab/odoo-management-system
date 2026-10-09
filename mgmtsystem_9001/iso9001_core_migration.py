# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Data migration: old iso9001.* tables -> the shared ISO core.

Before this change, ISO 9001 defined its own ``iso9001.clause``,
``iso9001.gap`` and ``iso9001.gap.line`` models. Those concepts now live in
``mgmtsystem_iso_base`` (``mgmtsystem.iso.clause`` / ``.gap`` / ``.gap.line``)
with ``standard_id`` distinguishing the standard.

This hook moves any existing rows into the core models, keyed on the clause
number / gap name so it can be re-run without creating duplicates. The old
tables are deliberately left in place (no DROP) so a rollback stays possible;
they simply stop being used.

The hook is a no-op on a fresh install, where the old tables never existed.
"""

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def _table_exists(cr, table):
    cr.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_name = %s AND table_schema = 'public'",
        (table,),
    )
    return bool(cr.fetchone())


def migrate_iso9001_to_core(cr, registry):
    """Move legacy ISO 9001 rows into the shared core models."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    standard = env.ref(
        "mgmtsystem_iso_base.iso_standard_9001", raise_if_not_found=False
    )
    if not standard:
        _logger.warning(
            "ISO 9001 standard not found in the core register; "
            "skipping legacy migration."
        )
        return

    Clause = env["mgmtsystem.iso.clause"]
    Gap = env["mgmtsystem.iso.gap"]
    GapLine = env["mgmtsystem.iso.gap.line"]

    # ── Clauses ─────────────────────────────────────────────
    if _table_exists(cr, "iso9001_clause"):
        cr.execute(
            "SELECT id, name, clause_number, description, parent_id, sequence, "
            "company_id FROM iso9001_clause ORDER BY id"
        )
        rows = cr.fetchall()
        clause_map = {}  # old id -> new id
        # First pass: create/update clauses without parents.
        for old_id, name, number, description, _parent, sequence, company in rows:
            existing = Clause.search(
                [("clause_number", "=", number), ("standard_id", "=", standard.id)],
                limit=1,
            )
            if existing:
                clause_map[old_id] = existing.id
                continue
            new = Clause.create({
                "name": name,
                "clause_number": number,
                "description": description,
                "sequence": sequence or 10,
                "standard_id": standard.id,
                "company_id": company,
            })
            clause_map[old_id] = new.id
        # Second pass: wire parents now that all clauses exist.
        for old_id, _n, _num, _d, parent, _s, _c in rows:
            if parent and parent in clause_map:
                Clause.browse(clause_map[old_id]).write({
                    "parent_id": clause_map[parent],
                })
        _logger.info("Migrated %s ISO 9001 clauses to the core.", len(rows))

    # ── Gap analyses ────────────────────────────────────────
    gap_map = {}  # old gap id -> new gap id
    if _table_exists(cr, "iso9001_gap"):
        cr.execute(
            "SELECT id, name, date, assessed_by, state, company_id, notes "
            "FROM iso9001_gap ORDER BY id"
        )
        rows = cr.fetchall()
        for old_id, name, date, assessed_by, state, company, notes in rows:
            existing = Gap.search(
                [
                    ("name", "=", name),
                    ("standard_id", "=", standard.id),
                    ("company_id", "=", company),
                ],
                limit=1,
            )
            if existing:
                gap_map[old_id] = existing.id
                continue
            new = Gap.create({
                "name": name,
                "date": date,
                "assessed_by": assessed_by,
                "state": state or "draft",
                "standard_id": standard.id,
                "company_id": company,
                "notes": notes,
            })
            gap_map[old_id] = new.id
        _logger.info("Migrated %s ISO 9001 gap analyses to the core.", len(rows))

    # ── Gap lines ───────────────────────────────────────────
    if _table_exists(cr, "iso9001_gap_line"):
        cr.execute(
            "SELECT id, gap_id, clause_id, maturity_level, finding, "
            "recommendation, status FROM iso9001_gap_line ORDER BY id"
        )
        rows = cr.fetchall()
        migrated = 0
        for _old_id, gap_id, clause_id, maturity, finding, rec, status in rows:
            new_gap_id = gap_map.get(gap_id)
            new_clause_id = clause_map.get(clause_id)
            if not new_gap_id or not new_clause_id:
                continue
            existing = GapLine.search(
                [
                    ("gap_id", "=", new_gap_id),
                    ("clause_id", "=", new_clause_id),
                ],
                limit=1,
            )
            if existing:
                continue
            GapLine.create({
                "gap_id": new_gap_id,
                "clause_id": new_clause_id,
                "maturity_level": maturity or "0",
                "finding": finding,
                "recommendation": rec,
                "status": status or "open",
            })
            migrated += 1
        _logger.info("Migrated %s ISO 9001 gap lines to the core.", migrated)
