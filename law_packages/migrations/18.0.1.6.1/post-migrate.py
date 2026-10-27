# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)

# Två trösklar vid 250 anställda:
#
# ÅRL 6:10 — hållbarhetsrapport. Kravet gäller företag som uppfyller
# minst två av tre: >250 anställda, >175 Mkr balansomslutning,
# >350 Mkr nettoomsättning. Vi sätter 250 som tröskel; de ekonomiska
# villkoren kan inte uttryckas i ett anställningstal och får bedömas
# manuellt.
#
# GDPR art. 37 / Dataskyddslagen — dataskyddsombud (DPO) krävs inte vid
# 250, men artikel 37.1 kräver DPO vid omfattande systematisk
# övervakning eller känsliga uppgifter. 250 är den praxisgräns där
# tillsynsmyndigheter förväntar sig en DPO. Föreskriften är alltså inte
# absolut — size_threshold är information, inte filter.
THRESHOLDS_250 = {
    '1995:1554': '250_employees',   # ÅRL — hållbarhetsrapport 6:10
    '2018:218': '250_employees',    # Dataskyddslagen — DPO i praktiken
}

# Revisionsplikt: ÅRL 9:1 — aktiebolag som uppfyller minst två av tre
# (>3 anställda i medeltal, >1,5 Mkr balans, >3 Mkr nettoomsättning)
# ska ha revisor. Tröskeln är 3 anställda i modellen.
THRESHOLDS_3 = {
    '1995:1554': '3_more_2yr',
}


def migrate(cr, version):
    if not version:
        return

    for sfs, threshold in THRESHOLDS_250.items():
        cr.execute(
            "UPDATE bpm_law_package_line SET size_threshold = %s WHERE sfs_number = %s",
            (threshold, sfs),
        )
        _logger.info('law_packages: size_threshold %s på %s %s-rader',
                     threshold, cr.rowcount, sfs)

    # LSO gäller alla verksamheter med lokal — ingen storlekströskel.
    # En rad hade 50_employees av misstag; den rensas.
    cr.execute(
        "UPDATE bpm_law_package_line SET size_threshold = NULL "
        "WHERE sfs_number = '2003:778'"
    )

    # Revisionsplikten ligger på revisorslagen, inte på ÅRL. Sätts bara
    # om raden finns och saknar tröskel.
    cr.execute(
        "UPDATE bpm_law_package_line SET size_threshold = '3_more_2yr' "
        "WHERE sfs_number = '2001:883' AND (size_threshold IS NULL OR size_threshold = '')"
    )
    if cr.rowcount:
        _logger.info('law_packages: size_threshold 3_more_2yr på %s revisorslags-rader',
                     cr.rowcount)
