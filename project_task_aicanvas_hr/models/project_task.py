import json
from langchain_core.messages import AIMessage
from odoo import models, api, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one('hr.department', string="Department")

    # def _canvas_params(self):
    #     params = f"""
    #         Generate quest data for this:
    #
    #         idea: {self.name}
    #         needs: {self.needs}
    #         solution: {self.solution}
    #     """
    #     return params
    #
    # def json2dict(self, text):
    #     json_split = text.split('```')
    #     if len(json_split) > 1:
    #         text = text.split('```')[1].replace("json", "").replace("\n", "").replace("'", '"')
    #         return json.loads(text)
    #     return eval(text)
    #
    # def _process_quest_data(self, bot_response):
    #     if bot_response.get('messages', False):
    #         messages = bot_response.get('messages', {})
    #     else:
    #         messages = bot_response.get('result', {})
    #     ai_messages = [m for m in messages if isinstance(m, AIMessage)]
    #     last_ai_message = ai_messages[-1] if len(ai_messages) != 0 else None
    #     message_content = last_ai_message.content
    #     return self.json2dict(message_content)

    def _action_create_project_task_quest(self):
        self.env['ai.quest'].create({
            'name': self.name,
            'sub_description': self.name,
            'ai_type': 'ai-staff',
            'department_id': self.department_id.id,
            'ai_agent_ids': [(0, 0, {
                'ai_agent_id': self.env.ref('project_task_aicanvas_hr.hr_department_ai_canva_agent').id,
            })]
        })
