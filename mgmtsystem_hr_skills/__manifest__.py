# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: HR Skills Integration',
    'version': '18.0.1.0.0',
    'license': 'AGPL-3',
    'summary': 'ISO-kompetenser och certifieringar i HR-skills',
    'category': 'Management',
    'depends': ['mgmtsystem', 'hr_skills'],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_skill_data.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': True,
}
