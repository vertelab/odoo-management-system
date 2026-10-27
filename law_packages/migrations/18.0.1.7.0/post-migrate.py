# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# Årsredovisningslagen saknades i sex av sju paket. Alla aktiebolag måste
# lämna årsredovisning — det är inte branschberoende. Bara consulting
# hade den.
#
# 6:10 hållbarhetsrapport: minst två av >250 anställda, >175 Mkr balans,
# >350 Mkr omsättning. Vi sätter 250 som tröskel; de ekonomiska villkoren
# kan inte uttryckas i ett anställningstal.
#
# 9:1 revisionsplikt: minst två av >3 anställda, >1,5 Mkr balans,
# >3 Mkr omsättning. Tröskeln 3_more_2yr sätts på revisorslagen.
PACKAGES = ['elevator', 'law_firm', 'manufacturing', 'restaurant', 'retail', 'webshop']

DESCRIPTION = (
    'Krav på årsredovisning, förvaltningsberättelse och revisionsberättelse. '
    '6:10 hållbarhetsrapport vid minst två av: >250 anställda, >175 Mkr balans, '
    '>350 Mkr omsättning. 9:1 revisionsplikt vid minst två av: >3 anställda, '
    '>1,5 Mkr balans, >3 Mkr omsättning.'
)


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    Line = env['bpm.law.package.line']
    Package = env['bpm.law.package']
    created = 0
    for pkg_type in PACKAGES:
        package = Package.search([('business_type', '=', pkg_type)], limit=1)
        if not package:
            continue
        if Line.search_count([('package_id', '=', package.id),
                              ('sfs_number', '=', '1995:1554')]):
            continue
        line = Line.create({
            'package_id': package.id,
            'name': 'Årsredovisningslag (1995:1554)',
            'sfs_number': '1995:1554',
            'department': 'Justitiedepartementet',
            'category': 'accounting',
            'description': DESCRIPTION,
            'sequence': 30,
            'min_employees': 1,
            'size_threshold': '250_employees',
        })
        env['ir.model.data'].create({
            'module': 'law_packages',
            'name': '%s_arl' % pkg_type,
            'model': 'bpm.law.package.line',
            'res_id': line.id,
            'noupdate': True,
        })
        created += 1
    _logger.info('law_packages: lade till ÅRL i %s paket', created)
