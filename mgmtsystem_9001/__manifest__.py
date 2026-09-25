# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO 9001:2026 — Kvalitetsledning',
    'version': '18.0.1.0.0',
    'summary': 'ISO 9001:2026 QMS — klausuler, gap-analys, kvalitetspolicy, kvalitetsmål, processer',
    'category': 'Management',
    'description': '''
ISO 9001:2026 — Kvalitetsledning
================================

    Quality Management System (QMS) per ISO 9001:2026.

Implements:

    - All clauses 4-10 with descriptions.
    - Gap analysis with maturity assessment (0-5) per clause.
    ''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_9001',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/iso9001_clause_data.xml',
        'data/iso9001_template_data.xml',
        'views/iso9001_clause_views.xml',
        'views/iso9001_policy_views.xml',
        'views/iso9001_gap_views.xml',
        'views/iso9001_objective_views.xml',
        'views/iso9001_process_views.xml',
        'views/iso9001_dashboard_views.xml',
        'views/iso9001_menu.xml',
        'views/res_config_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
