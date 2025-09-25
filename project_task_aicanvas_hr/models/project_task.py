import json
from langchain_core.messages import AIMessage
from odoo import models, api, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one('hr.department', string="Department")

    ai_quest_id = fields.Many2one(comodel_name='ai.quest', string="AI Quest", help="", readonly=True)

    def _action_create_project_task_quest(self):
        ai_quest_id = self.env['ai.quest'].create({
            'name': self.name,
            'sub_description': self.name,
            'ai_type': 'ai-staff',
            'department_id': self.department_id.id,
            'ai_agent_ids': [(0, 0, {
                'ai_agent_id': self.env.ref('project_task_aicanvas_hr.hr_department_ai_canva_agent').id,
            })],
            'code': """
    canva_id = self.env['project.task'].search([('ai_quest_id', '=', self.id)])
    result = quest.build(session=session, message=message_body, record=canva_id.id).invoke({"messages": [HumanMessage(content=message_body)]})
                """
        })
        self.ai_quest_id = ai_quest_id.id
