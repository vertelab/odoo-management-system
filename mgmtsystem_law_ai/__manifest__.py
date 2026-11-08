# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2026 Vertel Sverige AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Management System: Law AI',
    'version': '18.0.1.0.0',
    'summary': 'AI coworker for law texts — relevance assessment and summaries.',
    'category': 'Management',
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-management-system/mgmtsystem_law_ai',
    'license': 'AGPL-3',
    'description': '''
Management System: Law AI
==========================

    An AI coworker that works with the law register (document.law), following
    the same pattern as project_ai: one ai.coworker with specialist ai.agent
    children, skills that describe how the work is done, and tools that read
    and write Odoo records.

    Replaces three modules built on ai.quest (the pre-ai_agent_core model):

        mgmtsystem_law_ai_chat       — chat about a law
        mgmtsystem_law_ai_relevancy  — is this law relevant to us?
        mgmtsystem_law_ai_summary    — summarise the law for the reader

    ai.quest cannot coexist with ai_agent_core, so none of the three could be
    installed. They also pulled in langchain_openai / langchain_mistralai to
    call a model directly; the coworker uses the configured ai.provider
    instead, so no langchain and no API keys in code.

    Features:

        - Two buttons on the law form: Assess Relevance, Summarise
        - A chat entry point on the law form
        - Both actions also runnable from a cron (opt-in per company)
    ''',
    'depends': [
        'mgmtsystem',
        'document_law',
        'ai_agent_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/law_skills.xml',
        'data/law_agents.xml',
        'data/law_coworker.xml',
        'views/document_law_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
