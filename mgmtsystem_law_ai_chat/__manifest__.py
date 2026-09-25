# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) {year} {company} (<{mail}>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#
# https://www.odoo.com/documentation/14.0/reference/module.html
#
{
    'name': 'Management System: Law AI Chat',
    'version': '18.0.1.0.0',
    'summary': "Adds an AI chat for legal documents.",
    'category': 'Management',
    'description': '''
Law AI Chat
===========

    Adds an AI chat for legal documents.

    Features:

        - Extends Odoo: Builds on ai.agent, ai.quest, ai.quest.session, document.law.
    ''',
    #'sequence': 1,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_law_ai_chat',
    'images': ['static/description/banner.png'], # 560x280
    'license': 'AGPL-3',
    'depends': ["mgmtsystem_law", "ai_agent_core"],
    'data': [
        'data/ai_memory_data.xml',
        'data/ai_agent_data.xml',
        'data/ai_quest_data.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True,    
    'auto_install': False,
}
