from odoo import models, api, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one('hr.department', string="Department")

    # def action_create_ai_quest(self):
