# Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO 45001:2018 — Arbetsmiljöledning',
    'version': '18.0.1.0.2',
    'summary': 'ISO 45001 OHSMS — klausuler, gap-analys, arbetsmiljöpolicy, risker och möjligheter',
    'category': 'Management',
    'description': """
        Arbetsmiljöledningssystem (OHSMS) enligt ISO 45001:2018.

        Tunt skal ovanpå mgmtsystem_iso_base (den gemensamma ISO-kärnan):
        - Klausulerna 4–10 ligger i kärnans klausulmodell, kopplade till
          ISO 45001 i standardregistret
        - Gap-analys med mognadsbedömning (0–5) använder kärnans gap-modell
        - Arbetsskaderelaterade processer (unikt för 45001)

        Policy hanteras av mgmtsystem_manual / document_page och mål av
        mgmtsystem_objective — inga egna kopior. Risker och möjligheter
        hanteras av mgmtsystem_hazard / mgmtsystem_hazard_risk.

        Lagstiftning kopplas via mgmtsystem_law till document.law — AFS:er
        läses in som lagposter och refereras från klausuler och risker,
        aldrig hårdkodade i modulen.

        ISO 45001:2018 inkluderar:
        - Kontext och arbetstagardeltagande (5.4)
        - Risker och möjligheter kopplade till arbetsmiljöfaror (6.1.2)
        - Beredskap och agerande vid nödsituationer (8.2)
        - Uppföljning, mätning och utvärdering av efterlevnad (9.1)
    """,
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_45001',
    'license': 'AGPL-3',
    'depends': [
        'mgmtsystem_iso_base',
        'mgmtsystem_manual',
        'mgmtsystem_objective',
        'mgmtsystem_hazard',
        'mgmtsystem_hazard_risk',
        'mgmtsystem_law',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/iso45001_clause_data.xml',
        'views/iso45001_ohs_process_views.xml',
        'views/iso45001_dashboard_views.xml',
        'views/iso45001_menu.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
