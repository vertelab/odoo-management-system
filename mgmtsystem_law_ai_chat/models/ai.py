import re
import markdown
from markupsafe import Markup
from bs4 import BeautifulSoup
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError

import logging

_logger = logging.getLogger(__name__)



class AIQuestSession(models.Model):
    _inherit = 'ai.quest.session'

    ai_type = fields.Selection(
        selection_add=[('mgmt-law-chat', 'Chat with Management Law')],
        ondelete={'mgmt-law-chat': 'cascade'}
    )


class AIAgent(models.Model):
    _inherit = "ai.agent"

    ai_type = fields.Selection(
        selection_add=[('mgmt-law-chat', 'Chat with Management Law')],
        ondelete={'mgmt-law-chat': 'cascade'}
    )

    def agent_extra_context(self, quest, record=None):
        res = super().agent_extra_context(quest=quest, record=record)
        if self.ai_type == "mgmt-law-chat":
            document_law_id = self.env['document.law'].search([('ai_quest_id', '=', quest.id)], limit=1)
            if document_law_id:
                res['Management Law Title'] = document_law_id.rss_titel
                res['Management Law Content'] = document_law_id.rss_html
        return res




class AIQuest(models.Model):
    _inherit = "ai.quest"

    ai_type = fields.Selection(
        selection_add=[('mgmt-law-chat', 'Chat with Management Law')],
        ondelete={'mgmt-law-chat': 'cascade'}
    )

