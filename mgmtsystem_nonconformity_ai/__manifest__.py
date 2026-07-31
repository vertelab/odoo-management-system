# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2025- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
##############################################################################

{
    'name': 'Management Nonconformity: Chat with Nonconformity',
    'version': '18.0.1.0.0',
    'summary': 'AI-coworker per nonconformity (chat via discuss.channel)',
    'category': 'helpdesk',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_nonconformity_ai',
    'license': 'AGPL-3',
    'depends': [
        'mgmtsystem_nonconformity',
        'ai_agent_core',
    ],
    'data': [
        'data/ai_coworker_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
