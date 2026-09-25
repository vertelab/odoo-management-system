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
    'version': '18.0.1.0.0',
    'summary': """Management System YearWheel.""",
    'category': 'management',
    'description': '''
YearWheel
=========

    Management System YearWheel.

    Features:

        - Automation: Scheduled jobs: Year Wheel: Activity Manager, Year Wheel: Activity Manager.
        - Guided Wizards: Step-by-step dialogs for data entry.
        - UI Integration: Extends 6 view(s) in the Odoo interface.
        - Extends Odoo: Builds on mail.activity, mail.thread, summary, year.wheel.
    ''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_yearwheel',
    'images': ['static/description/banner.png'],  # 560x280
    'license': 'AGPL-3',
    'depends': 
        [
            "mgmtsystem", 
            "mail",
            #"mgmtsystem_audit"
        ],
    'data': [
        "views/year_wheel_view.xml",
        "wizard/year_wheel_wizard_view.xml",
        "views/menu_view.xml",
        #"views/mgmtsystem_audit_view.xml",
        "data/ir_cron.xml",
        "security/ir.model.access.csv"
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
