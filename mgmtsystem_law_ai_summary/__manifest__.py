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
    'name': 'Management System: Law AI Summary',
    'version': '18.0.1.0.0',
    'summary': "Summarises legal documents with AI.",
    'category': 'Management',
    'description': '''
Law AI Summary
==============

    Summarises legal documents with AI.

    Features:

        - Automation: Scheduled jobs: Create AI Summarys of Laws, Create AI Summarys of Laws.
        - UI Integration: Extends 2 view(s) in the Odoo interface.
        - Extends Odoo: Builds on ai.agent, ai.quest, document.law.
    ''',
    #'sequence': 1,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_law_ai_summary',
    'images': ['static/description/banner.png'], # 560x280
    'license': 'AGPL-3',
    'depends': ["mgmtsystem_law", "ai_agent_core"],
    'data': 
    [
        "data/ai_data.xml",
        "data/cron.xml",
        "views/document_law_views.xml"
    ],
    'demo': [],
    'application': False,
    'installable': True,    
    'auto_install': False,
    #"post_init_hook": "post_init_hook",
}
