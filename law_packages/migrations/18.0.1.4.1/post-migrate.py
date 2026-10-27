# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# AFS 2023:12 och LSO 2003:778 lades till i fem paket som saknade dem.
# Datafilerna har noupdate="1" och laddas inte vid uppgradering, så
# raderna skapas här i stället. xmlid:t sätts så att en framtida
# installation inte dubbelskapar dem.
NEW_LINES = [
    ('consulting', 'afs_2023_12', 'AFS 2023:12 — Utformning av arbetsplatser', 'AFS 2023:12', 'Arbetsmiljöverket', 'employment', 90,
     '4 kap. 3 §: rutiner för utrymning och utrymningsövningar.'),
    ('consulting', 'lso', 'Lag om skydd mot olyckor (2003:778)', '2003:778', 'Justitiedepartementet', 'safety', 95,
     '2 kap. 2 §: systematiskt brandskyddsarbete (SBA).'),
    ('elevator', 'afs_2023_12', 'AFS 2023:12 — Utformning av arbetsplatser', 'AFS 2023:12', 'Arbetsmiljöverket', 'employment', 90,
     '4 kap. 3 §: rutiner för utrymning och utrymningsövningar.'),
    ('elevator', 'lso', 'Lag om skydd mot olyckor (2003:778)', '2003:778', 'Justitiedepartementet', 'safety', 95,
     '2 kap. 2 §: systematiskt brandskyddsarbete (SBA).'),
    ('law_firm', 'afs_2023_12', 'AFS 2023:12 — Utformning av arbetsplatser', 'AFS 2023:12', 'Arbetsmiljöverket', 'employment', 90,
     '4 kap. 3 §: rutiner för utrymning och utrymningsövningar.'),
    ('law_firm', 'lso', 'Lag om skydd mot olyckor (2003:778)', '2003:778', 'Justitiedepartementet', 'safety', 95,
     '2 kap. 2 §: systematiskt brandskyddsarbete (SBA).'),
    ('manufacturing', 'afs_2023_12', 'AFS 2023:12 — Utformning av arbetsplatser', 'AFS 2023:12', 'Arbetsmiljöverket', 'employment', 90,
     '4 kap. 3 §: rutiner för utrymning och utrymningsövningar.'),
    ('manufacturing', 'lso', 'Lag om skydd mot olyckor (2003:778)', '2003:778', 'Justitiedepartementet', 'safety', 95,
     '2 kap. 2 §: systematiskt brandskyddsarbete (SBA).'),
    ('webshop', 'afs_2023_12', 'AFS 2023:12 — Utformning av arbetsplatser', 'AFS 2023:12', 'Arbetsmiljöverket', 'employment', 90,
     '4 kap. 3 §: rutiner för utrymning och utrymningsövningar.'),
    ('webshop', 'lso', 'Lag om skydd mot olyckor (2003:778)', '2003:778', 'Justitiedepartementet', 'safety', 95,
     '2 kap. 2 §: systematiskt brandskyddsarbete (SBA).'),
    ('restaurant', 'afs_2023_12', 'AFS 2023:12 — Utformning av arbetsplatser', 'AFS 2023:12', 'Arbetsmiljöverket', 'employment', 90,
     '4 kap. 3 §: rutiner för utrymning och utrymningsövningar.'),
    ('retail', 'afs_2023_12', 'AFS 2023:12 — Utformning av arbetsplatser', 'AFS 2023:12', 'Arbetsmiljöverket', 'employment', 90,
     '4 kap. 3 §: rutiner för utrymning och utrymningsövningar.'),
]


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    Line = env['bpm.law.package.line']
    Package = env['bpm.law.package']
    created = 0
    for pkg_type, xmlid, name, sfs, dept, cat, seq, desc in NEW_LINES:
        package = Package.search([('business_type', '=', pkg_type)], limit=1)
        if not package:
            continue
        if Line.search_count([('package_id', '=', package.id),
                              ('sfs_number', '=', sfs)]):
            continue
        line = Line.create({
            'package_id': package.id,
            'name': name,
            'sfs_number': sfs,
            'department': dept,
            'category': cat,
            'description': desc,
            'sequence': seq,
            'min_employees': 1,
        })
        env['ir.model.data'].create({
            'module': 'law_packages',
            'name': '%s_%s' % (pkg_type, xmlid),
            'model': 'bpm.law.package.line',
            'res_id': line.id,
            'noupdate': True,
        })
        created += 1
    _logger.info('law_packages: skapade %s nya lagrader (AFS 2023:12, LSO)', created)
