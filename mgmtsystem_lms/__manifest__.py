# Copyright (C) 2025 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Management System: LMS Training Integration',
    'version': '18.0.1.0.0',
    'summary': 'ISO-standardkurser via website_slides med certifiering',
    'category': 'Management',
    'depends': ['mgmtsystem', 'website_slides'],
    'data': [
        'security/ir.model.access.csv',
        'data/slide_channel_data.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': True,
}
