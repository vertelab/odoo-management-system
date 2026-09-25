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
    'name': 'Management System: Project AI Canvas HR',
    'version': '18.0.1.0.0',
    'summary': """Project AI Canvas HR.""",
    'category': 'Management',
    'description': '''
Project AI Canvas HR
====================

    Project AI Canvas HR.

    Features:

        - UI Integration: Extends 6 view(s) in the Odoo interface.
        - Extends Odoo: Builds on ai.agent, ai.coworker, hr.department, project.task.
    ''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/project_task_aicanvas_hr',
    'images': ['static/description/banner.png'],  # 560x280
    'license': 'AGPL-3',
    'depends':
        [
            "ai_agent_core",
        ],
    'data': [
        'views/project_task_views.xml',
        'views/hr_department_views.xml',
        'views/ai_agent_views.xml',

        # data
        'data/ai_agent_data.xml',
    ],
    'demo': [ ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
