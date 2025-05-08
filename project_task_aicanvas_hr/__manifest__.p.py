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
#
{
    'name': 'Project AI Canvas HR',
    'version': '1.0',
    'summary': """Project AI Canvas HR""",
    'category': 'management',
    'description': """
        Project/Task AI Canvas HR
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-ai',
    'images': ['static/description/banner.png'],  # 560x280
    'license': 'AGPL-3',
    'depends':
        [
            "ai_agent_hr",
        ],
    'data': [
        'views/project_task_views.xml',
        'views/hr_department_views.xml',

        # data
        'data/ai_agent_data.xml',
        'data/ai_quest_data.xml',
    ],
    'demo': [ ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
