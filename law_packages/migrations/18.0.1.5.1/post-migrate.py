# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)

# Skyddskommitté: AML 6:8 — "Vid en arbetsplats där minst femtio
# arbetstagare sysselsätts stadigvarande ska det finnas en
# skyddskommitté."
#
# Tröskeln hör till AML, inte till AFS-föreskrifterna. Vi sätter den
# därför som size_threshold på AML-raden — information till användaren
# om varför lagen är med — och inte som min_employees, som skulle
# filtrera bort lagen för mindre företag. AML gäller alla.
THRESHOLD_50 = ['1977:1160']

# Lagar som gäller alla arbetsgivare. Fältet lämnades 0 av misstag på
# många rader, vilket gör att wizarden filtrerar bort dem när
# employee_count är 0.
ALL_EMPLOYERS = [
    '1977:1166', '1982:673', '1982:80',
    'AFS 2023:10', 'AFS 2023:11', 'AFS 2023:12', 'AFS 2023:13',
    'BFS 2025:11', 'BFS 2025:13',
    'ELSÄK-FS 2022:3', 'ELSÄK-FS 2022:5',
    '2003:778', '2010:1011', '2016:732',
]


def migrate(cr, version):
    if not version:
        return

    for sfs in THRESHOLD_50:
        cr.execute(
            "UPDATE bpm_law_package_line SET size_threshold = '50_employees' "
            "WHERE sfs_number = %s",
            (sfs,),
        )
        _logger.info('law_packages: size_threshold 50_employees på %s %s-rader',
                     cr.rowcount, sfs)

    for sfs in ALL_EMPLOYERS:
        cr.execute(
            "UPDATE bpm_law_package_line SET min_employees = 1 "
            "WHERE sfs_number = %s AND (min_employees IS NULL OR min_employees = 0)",
            (sfs,),
        )
