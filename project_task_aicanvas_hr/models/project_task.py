import json
from odoo import models, api, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one('hr.department', string="Department")
    ai_coworker_id = fields.Many2one(
        comodel_name='ai.coworker', string="AI Coworker", readonly=True)

    def _action_create_project_task_coworker(self):
        coworker = self.env['ai.coworker'].create({
            'name': self.name,
            'sub_description': self.name,
            'status': 'active',
            'orchestration_mode': 'single',
        })
        # Assign the HR canvas agent
        agent_ref = self.env.ref(
            'project_task_aicanvas_hr.hr_department_ai_canva_agent',
            raise_if_not_found=False)
        if agent_ref:
            self.env['ai.coworker.agent'].create({
                'coworker_id': coworker.id,
                'agent_id': agent_ref.id,
                'role': 'member',
            })
        self.ai_coworker_id = coworker.id
