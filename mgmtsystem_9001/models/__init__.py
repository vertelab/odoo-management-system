# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# ISO 9001 is a shell on top of mgmtsystem_iso_base:
#   - clauses live in mgmtsystem.iso.clause (core)
#   - gap analyses live in mgmtsystem.iso.gap (core)
#   - policy -> mgmtsystem_manual / document_page
#   - objectives -> mgmtsystem_objective
# Only the process model is unique to ISO 9001 and stays here.
from . import iso9001_process
from . import res_config
