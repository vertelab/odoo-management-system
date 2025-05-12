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
    'name': 'Management System: YearWheel',
    'version': '1.0',
    'summary': """Management System YearWheel""",
    'category': 'management',
    'description': """
        Management System YearWheel
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_yearwheel',
    'images': ['static/description/banner.png'],  # 560x280
    'license': 'AGPL-3',
    'depends': 
        [
            "mgmtsystem", 
            "mail",
            # #if VERSION >= "18.0"
            #"mgmtsystem_audit"
            # #elif VERSION < "18.0"
            "mgmtsystem_audit"
            # #endif
        ],
    'data': [
        "views/year_wheel_view.xml",
        "wizard/year_wheel_wizard_view.xml",
        "views/menu_view.xml",
        # #if VERSION >= "18.0"
        #"views/mgmtsystem_audit_view.xml",
        # #elif VERSION < "18.0"
        "views/mgmtsystem_audit_view.xml",
        # #endif
        "data/ir_cron.xml",
        "security/ir.model.access.csv"
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
