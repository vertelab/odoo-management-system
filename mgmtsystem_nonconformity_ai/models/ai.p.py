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
        selection_add=[('nonconformity-chat', 'Chat with Nonconformity')],
        ondelete={'nonconformity-chat': 'cascade'}
    )


class AIAgent(models.Model):
    _inherit = "ai.agent"

    ai_type = fields.Selection(
        selection_add=[('nonconformity-chat', 'Chat with Nonconformity')],
        ondelete={'nonconformity-chat': 'cascade'}
    )

    # def agent_extra_context(self, quest, record=None):
    #     res = super().agent_extra_context(quest=quest, record=record)
    #     if self.ai_type == "nonconformity-chat":
    #         mgmtsystem_nonconformity_id = self.env['mgmtsystem.nonconformity'].search([
    #             ('ai_quest_id', '=', quest.id)
    #         ], limit=1)
    #     return res




class AIQuest(models.Model):
    _inherit = "ai.quest"

    ai_type = fields.Selection(
        selection_add=[('nonconformity-chat', 'Chat with Nonconformity')],
        ondelete={'nonconformity-chat': 'cascade'}
    )

    # def server_action(self, records):
    #     if self.init_type == 'server-action' and self.server_action_id:
    #         if self._check_quest_error():
    #             raise UserError(self._check_quest_error())
    #         vals = self._server_action_values(records=records)
    #
    #         for record in records:
    #             prompt = f"What is the solution to this helpdesk ticket: {record.number}"
    #             result = self.run(prompt=prompt, record=record)
    #             if result:
    #                 ai_messages = self._get_last_ai_message(result.get('result', {}).get('messages', False))
    #                 answer = re.sub(
    #                     r'<think>.*?</think>', '', markdown.markdown(ai_messages.content), flags=re.DOTALL)
    #                 record.with_user(SUPERUSER_ID).message_post(
    #                     body=Markup(answer),
    #                     message_type='comment',
    #                     subtype_xmlid='mail.mt_comment',
    #                 )

