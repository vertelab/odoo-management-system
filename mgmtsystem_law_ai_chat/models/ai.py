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


class AIQuest(models.Model):
    _inherit = "ai.quest"

    ai_type = fields.Selection(
        selection_add=[('mgmt-law-chat', 'Chat with Management Law')],
        ondelete={'mgmt-law-chat': 'cascade'}
    )

