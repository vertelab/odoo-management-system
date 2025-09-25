from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from langchain_core.messages import AIMessage



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
        return self.json2dict(message_content)

    def _action_create_project_task_ai_canvas_idea(self, record, canvas: dict):
        canvas = canvas.get('canvas', {})

        if not record.project_id:
            raise UserError(_(f"Kindly select a Project on the department - {record.name} before you continue..."))
        if not canvas:
            return

        for canva in canvas:
            vals = {}

            if idea := canva.get('ideas'):
                ai_capability_ids = self.env['ai.canvas.capability']

                for capability in idea.get('ai_capability'):
                    ai_capability_ids += ai_capability_ids.search([
                        ('name', '=', capability
                         )], limit=1)

                if idea.get('implementation_type') and isinstance(idea.get('implementation_type'), list):
                    implementation_type = idea.get('implementation_type')[0]
                else:
                    implementation_type = idea.get('implementation_type')

                vals.update({
                    'name': idea.get('idea'),
                    'needs': idea.get('needs'),
                    'solution': idea.get('solution'),
                    'project_id': record.project_id.id,
                    'department_id': record.id,
                    'ai_capability': [(4, ai_capability_id.id, False) for ai_capability_id in ai_capability_ids],
                    'implementation_type': implementation_type,
                })

            if evaluation := canva.get('evaluation'):
                vals.update({
                    'value': evaluation.get('value'),
                    'value_point': str(evaluation.get('value_point')),
                    'feasibility_point': str(evaluation.get('feasibility_point')),
                    'feasibility': evaluation.get('feasibility'),

                })
            self.env['project.task'].create(vals)