# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_onboarding',
    'name': 'Management System: Onboarding Integration',
    'version': '18.0.1.0.0',
    'license': 'AGPL-3',
    'summary': 'ISO-specifika onboarding-moment för nyanställda',
    'description': '''
Onboarding Integration
======================

    ISO-specifika onboarding-moment för nyanställda.

    Features:

        - UI Integration: Extends 1 view(s) in the Odoo interface.
        - Extends Odoo: Builds on hr.onboarding.template.
    ''',
    'category': 'Management',
    'depends': ['mgmtsystem', 'hr_onboarding_ce'],
    'data': [
        'security/ir.model.access.csv',
        'data/onboarding_step_data.xml',
        'views/hr_onboarding_template_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': True,
}
