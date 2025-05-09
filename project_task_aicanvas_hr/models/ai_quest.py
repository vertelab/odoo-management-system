import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from langchain_core.messages import AIMessage

_logger = logging.getLogger(__name__)

class AIQuest(models.Model):
    _inherit = "ai.quest"

    def _action_get_ai_canvas_idea(self, bot_response):
        if bot_response.get('messages', False):
            messages = bot_response.get('messages', {})
        else:
            messages = bot_response.get('result', {})
        ai_messages = [m for m in messages if isinstance(m, AIMessage)]
        last_ai_message = ai_messages[-1] if len(ai_messages) != 0 else None
        message_content = last_ai_message.content
        _logger.info(f"{message_content=}")
        return self.json2dict(message_content)

    def _action_create_project_task_ai_canvas_idea(self, record, ideas: dict):
        ideas = ideas.get('ideas', {})
        if not record.project_id:
            raise UserError(_(f"Kindly select a Project on the department - {record.name} before you continue..."))
        if not ideas:
            return
        _logger.info(f"{ideas=}")
        for idea in ideas:
            self.env['project.task'].create({
                'name': idea.get('idea'),
                'needs': idea.get('needs'),
                'solution': idea.get('solution'),
                'project_id': record.project_id.id,
                'department_id': record.id,
            })
