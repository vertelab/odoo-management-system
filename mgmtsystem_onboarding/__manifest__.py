# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: Onboarding Integration',
    'version': '18.0.1.0.0',
    'summary': 'ISO-specifika onboarding-moment för nyanställda',
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
