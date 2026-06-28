# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: Security Alert Monitoring',
    'version': '18.0.1.0.0',
    'summary': 'Automatisk säkerhetsbevakning — CERT-SE, NCSC, CVE/NVD, Ubuntu USN',
    'category': 'Management',
    'description': """
        Automatisk säkerhetsbevakning för ledningssystemet.

        Hämtar säkerhetsvarningar från fyra källor:
        - CERT-SE (Atom RSS)
        - NCSC Aktuellt (web scraping)
        - NVD CVE (REST API v2.0)
        - Ubuntu Security Notices (REST API)

        Funktioner:
        - Automatisk schemalagd inhämtning (cron)
        - Programvaruinventering för CVE-filtrering
        - AI-relevansbedömning av varningar
        - Koppling till ISO 27001 Annex A-kontroller
        - Koppling till EBIOS security events
        - Åtgärdshantering via mgmtsystem.action
        - Dashboard med pivot/grafer

        Kräver pip-paket: feedparser, beautifulsoup4, requests
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_security_alert',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'mgmtsystem',
        'mgmtsystem_security_event',
        'mgmtsystem_action',
    ],
    'external_dependencies': {
        'python': ['feedparser', 'beautifulsoup4', 'requests'],
    },
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/security_alert_source_data.xml',
        'data/cron.xml',
        'data/ai_agent_data.xml',
        'views/security_alert_source_views.xml',
        'views/security_alert_views.xml',
        'views/security_alert_rule_views.xml',
        'views/security_alert_dashboard_views.xml',
        'views/security_software_views.xml',
        'views/security_alert_menu.xml',
        'views/res_config_views.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
