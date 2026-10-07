# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO 27001:2022 — Informationssäkerhet',
    'version': '18.0.1.0.1',
    'summary': 'ISO 27001:2022 ISMS — mallar, gap-analys, SoA och Annex A kontroller.',
    'category': 'Management',
    'description': '''
ISO 27001:2022 — Informationssäkerhet
=====================================

    Information Security Management System (ISMS) per ISO 27001:2022.

Implements:

    - All 93 Annex A controls (5.1-8.34) with descriptions.
    - Gap analysis with maturity assessment (0-5) per control.
    ''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_27001',
    'license': 'AGPL-3',
    'depends': [
        'mgmtsystem',
        'mgmtsystem_manual',
        'mgmtsystem_info_security_manual',
        'mgmtsystem_information_security',
        'mgmtsystem_security_event',
        'mgmtsystem_risk',
        'mgmtsystem_action',
        'mgmtsystem_audit',
        'mgmtsystem_review',
        'mgmtsystem_nonconformity',
        'mgmtsystem_kpi',
        'mail',
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/iso27001_annex_a_data.xml',
        'data/iso27001_clause_data.xml',
        'data/iso27001_template_data.xml',
        'views/iso27001_control_views.xml',
        'views/iso27001_gap_views.xml',
        'views/iso27001_soa_views.xml',
        'views/iso27001_clause_views.xml',
        'views/iso27001_policy_views.xml',
        'views/iso27001_dashboard_views.xml',
        'views/mgmtsystem_action_views.xml',
        'views/mgmtsystem_audit_views.xml',
        'views/res_config_views.xml',
        'views/iso27001_menu.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
