# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO 42001:2023 — AI-ledningssystem',
    'version': '18.0.1.0.0',
    'summary': 'ISO 42001:2023 AIMS — klausuler, AI-systemregister, konsekvensbedömning, Annex A kontroller, SoA',
    'category': 'Management',
    'description': """
        Ledningssystem för artificiell intelligens (AIMS) enligt ISO/IEC 42001:2023.

        Implementerar:
        - Samtliga klausuler 4–10 med svenska beskrivningar
        - Annex A referenskontroller (A.2–A.10) med svenska beskrivningar
        - AI-systemregister — dokumentation av samtliga AI-system
        - AI-konsekvensbedömning — fairness, transparency, privacy, safety, bias
        - Statement of Applicability (SoA) med koppling till Annex A
        - Gap-analys med mognadsbedömning (maturity 0–5)
        - AI-policy med signeringsflöde
        - AI-mål (Annex C) — mätbara mål för AI-governance
        - Dashboard för AIMS-status

        ISO/IEC 42001:2023 är den första internationella standarden för AI-ledningssystem.
        Alla fyra annex (A, B, C, D) är informativa — Annex A är referenskontroller
        (ej normativa som i 27001) men granskas ändå vid certifiering.

        Bygger på OCA mgmtsystem-moduler. Ingen befintlig AI-modul finns i OCA —
        detta är helt nytt.
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_42001',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/iso42001_clause_data.xml',
        'data/iso42001_annex_a_data.xml',
        'data/iso42001_template_data.xml',
        'views/iso42001_clause_views.xml',
        'views/iso42001_policy_views.xml',
        'views/iso42001_gap_views.xml',
        'views/iso42001_control_views.xml',
        'views/iso42001_aisystem_views.xml',
        'views/iso42001_impact_assessment_views.xml',
        'views/iso42001_soa_views.xml',
        'views/iso42001_objective_views.xml',
        'views/iso42001_dashboard_views.xml',
        'views/iso42001_menu.xml',
        'views/res_config_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
