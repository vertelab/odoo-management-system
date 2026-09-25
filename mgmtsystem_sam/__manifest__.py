# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: Systematiskt Arbetsmiljöarbete (SAM)',
    'version': '18.0.1.0.0',
    'summary': 'Systematiskt Arbetsmiljöarbete enligt ISO 45001 och AFS 2023:1',
    'category': 'Management',
    'description': '''
Systematiskt Arbetsmiljöarbete (SAM)
====================================

    Systematic Work Environment Management (SAM) per ISO 45001:2018 and AFS 2023:1.

Implements the 8 steps of the SAM process:

    1. Work environment policy
    2. Delegation of duties
    3. Investigation / risk assessment
    4. Action plan
    5. Follow-up
    6. Annual review
    7. Documentation
    8. Continuous improvement
    ''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_sam',
    'license': 'AGPL-3',
    'depends': [
        'mgmtsystem',
        'mgmtsystem_hazard',
        'mgmtsystem_hazard_risk',
        'mgmtsystem_nonconformity',
        'mgmtsystem_action',
        'mgmtsystem_audit',
        'mgmtsystem_review',
        'mgmtsystem_yearwheel',
        'hr',
        'mail',
        'ai_agent_hr',
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sam_iso_clause_data.xml',
        'data/sam_hazard_type_data.xml',
        'data/sam_template_data.xml',
        'data/ai_agent_data.xml',
        'views/sam_iso_clause_views.xml',
        'views/sam_policy_views.xml',
        'views/sam_task_delegation_views.xml',
        'views/sam_instruction_views.xml',
        'views/sam_consultation_views.xml',
        'views/mgmtsystem_hazard_views.xml',
        'views/mgmtsystem_nonconformity_views.xml',
        'views/mgmtsystem_action_views.xml',
        'views/mgmtsystem_audit_views.xml',
        'views/mgmtsystem_review_views.xml',
        'views/sam_menu.xml',
        'views/sam_dashboard_views.xml',
        'views/res_config_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
