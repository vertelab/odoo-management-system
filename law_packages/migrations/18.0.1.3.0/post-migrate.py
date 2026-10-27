# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)

# Lagarna ligger i datafiler med noupdate="1" — de laddas vid första
# installationen och aldrig igen. Att lägga till min_employees i XML:en
# räcker därför inte för en databas som redan har posterna. Vi sätter
# fältet här i stället, en gång.
#
# Trösklarna: AML 6:2 (skyddsombud 5), AML 6:8 (skyddskommitté 50),
# AFS 2020:5 (arbetsanpassning 10). Grundläggande lagar gäller alla.
THRESHOLDS = {
    '1977:1160': 1,
    '1977:1166': 1,
    '1982:673': 1,
    '1982:80': 1,
    'AFS 2020:5': 10,
    'AFS 2023:10': 1,
    'AFS 2023:11': 1,
    'AFS 2023:13': 1,
    '2016:732': 1,
    '2010:900': 1,
    '2011:338': 1,
    'BFS 2025:11': 1,
    'BFS 2025:13': 1,
    'ELSÄK-FS 2022:3': 1,
    'ELSÄK-FS 2022:5': 1,
}


def migrate(cr, version):
    if not version:
        return
    updated = 0
    for sfs, n in THRESHOLDS.items():
        cr.execute(
            "UPDATE bpm_law_package_line SET min_employees = %s "
            "WHERE sfs_number = %s AND (min_employees IS NULL OR min_employees = 0)",
            (n, sfs),
        )
        updated += cr.rowcount
    _logger.info('law_packages: satte min_employees på %s lagrader', updated)
