# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO 14001:2026 — Miljöledning',
    'version': '18.0.1.0.0',
    'summary': 'ISO 14001:2026 EMS — klausuler, gap-analys, miljöpolicy, aspekter, lagkrav',
    'category': 'Management',
    'description': '''
ISO 14001:2026 — Miljöledning
=============================

    Environmental Management System (EMS) per ISO 14001:2026 (Edition 4).

Implements:

    - All clauses 4-10 with descriptions.
    - Gap analysis with maturity assessment (0-5) per clause.
    ''',
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
