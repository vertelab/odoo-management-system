# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Versioned migration: legacy iso9001.* -> shared ISO core.

Runs when an existing installation is upgraded to 18.0.1.1.0 (the version
that turns mgmtsystem_9001 into a shell on top of mgmtsystem_iso_base).
"""

from odoo.addons.mgmtsystem_9001.iso9001_core_migration import (
    migrate_iso9001_to_core,
)


def migrate(cr, version):
    migrate_iso9001_to_core(cr, None)
