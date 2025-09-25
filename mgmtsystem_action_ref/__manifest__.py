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
    'name': 'Management System: Action Ref',
    'version': '1.0',
    'summary': """
        Makes it possible to link action to any odoo model and record.
    """,
    'category': 'Management',
    'description': """
        Makes it possible to link action to any odoo model and record.
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_action_ref/',
    'license': 'AGPL-3',
    'depends': ["mgmtsystem_action"],
    'data': [
        "views/mgmtsystem_action_views.xml",
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
