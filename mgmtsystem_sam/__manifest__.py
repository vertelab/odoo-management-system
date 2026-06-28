# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: Systematiskt Arbetsmiljöarbete (SAM)',
    'version': '18.0.1.0.0',
    'summary': 'Systematiskt Arbetsmiljöarbete enligt ISO 45001 och AFS 2023:1',
    'category': 'Management',
    'description': """
        Systematiskt Arbetsmiljöarbete (SAM) enligt ISO 45001:2018 och AFS 2023:1.

        Implementerar SAM-processens 8 steg:
        1. Arbetsmiljöpolicy
        2. Uppgiftsfördelning
        3. Undersökning / riskbedömning
        4. Åtgärder / handlingsplan
        5. Kontroll / uppföljning
        6. Skyddsronder
        7. Tillbudsrapportering
        8. Årlig uppföljning

        Bygger på OCA mgmtsystem-moduler och Vertels egna tillägg.
        Integrerar AI-stöd via ai_agent för riskbedömning och incidentanalys.
        Använder Discuss-kanaler för medverkan enligt ISO 45001 5.4.
    """,
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
