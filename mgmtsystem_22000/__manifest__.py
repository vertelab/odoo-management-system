# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: ISO 22000:2018 — Livsmedelssäkerhet',
    'version': '18.0.1.0.0',
    'summary': 'ISO 22000:2018 FSMS — klausuler, gap-analys, policy, PRP, HACCP, CCP, spårbarhet',
    'category': 'Management',
    'description': """
        Ledningssystem för livsmedelssäkerhet (FSMS) enligt ISO 22000:2018.

        Implementerar:
        - Samtliga klausuler 4–10 med svenska beskrivningar
        - Gap-analys med mognadsbedömning (maturity 0–5) per klausul
        - Livsmedelssäkerhetspolicy med signeringsflöde
        - Grundförutsättningar (PRP) — hygien, rengöring, infrastruktur
        - HACCP-planer med faroanalys
        - Kritiska styrpunkter (CCP) med övervakning och korrigerande åtgärder
        - Flödesscheman för produktionskedjan
        - Spårbarhetstest (framåt/bakåt)
        - Nödberedskap och recall-planer
        - Livsmedelssäkerhetsmål med KPI:er
        - Dashboard för FSMS-status

        Bygger på OCA mgmtsystem-moduler.
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_22000',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'mgmtsystem',
        'mgmtsystem_action',
        'mgmtsystem_nonconformity',
        'mgmtsystem_audit',
        'mgmtsystem_review',
        'mgmtsystem_kpi',
        'product',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/iso22000_clause_data.xml',
        'data/iso22000_template_data.xml',
        'views/iso22000_clause_views.xml',
        'views/iso22000_policy_views.xml',
        'views/iso22000_gap_views.xml',
        'views/iso22000_objective_views.xml',
        'views/iso22000_prp_views.xml',
        'views/iso22000_haccp_views.xml',
        'views/iso22000_ccp_views.xml',
        'views/iso22000_hazard_views.xml',
        'views/iso22000_flow_views.xml',
        'views/iso22000_traceability_views.xml',
        'views/iso22000_emergency_views.xml',
        'views/iso22000_dashboard_views.xml',
        'views/iso22000_menu.xml',
        'views/res_config_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
