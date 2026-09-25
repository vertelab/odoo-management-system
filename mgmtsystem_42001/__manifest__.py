# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO 42001:2023 — AI-ledningssystem',
    'version': '18.0.1.0.0',
    'summary': 'ISO 42001:2023 AIMS — klausuler, AI-systemregister, konsekvensbedömning, Annex A kontroller, SoA',
    'category': 'Management',
    'description': '''
ISO 42001:2023 — AI-ledningssystem
==================================

    Artificial Intelligence Management System (AIMS) per ISO/IEC 42001:2023.

Implements:

    - All clauses 4-10 with descriptions.
    - Annex A reference controls (A.2-A.x).
    ''',
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
