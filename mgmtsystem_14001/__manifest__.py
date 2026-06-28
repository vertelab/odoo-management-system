# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO 14001:2026 — Miljöledning',
    'version': '18.0.1.0.0',
    'summary': 'ISO 14001:2026 EMS — klausuler, gap-analys, miljöpolicy, aspekter, lagkrav',
    'category': 'Management',
    'description': """
        Miljöledningssystem (EMS) enligt ISO 14001:2026 (Edition 4).

        Implementerar:
        - Samtliga klausuler 4–10 med svenska beskrivningar
        - Gap-analys med mognadsbedömning (maturity 0–5) per klausul
        - Miljöpolicy med signeringsflöde
        - Miljöaspekter och miljöpåverkan med livscykelperspektiv
        - Lagkravsregister (compliance obligations)
        - Miljömål och handlingsplaner
        - Dashboard för EMS-status

        ISO 14001:2026 (Edition 4, publicerad april 2026) inkluderar:
        - Förtydligade krav kring miljöaspekter och livscykelperspektiv
        - Förstärkt fokus på klimatförändringar och biologisk mångfald
        - Uppdaterad Annex SL-struktur
        - Förbättrad integration med andra ledningssystem

        Bygger på OCA mgmtsystem-moduler (mgmtsystem_environment,
        document_page_environmental_aspect).
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_14001',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/iso14001_clause_data.xml',
        'data/iso14001_template_data.xml',
        'views/iso14001_clause_views.xml',
        'views/iso14001_policy_views.xml',
        'views/iso14001_gap_views.xml',
        'views/iso14001_aspect_views.xml',
        'views/iso14001_compliance_views.xml',
        'views/iso14001_objective_views.xml',
        'views/iso14001_dashboard_views.xml',
        'views/iso14001_menu.xml',
        'views/res_config_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
