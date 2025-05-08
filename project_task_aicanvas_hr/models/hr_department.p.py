from odoo import models, api, fields


class HRDepartment(models.Model):
    _inherit = 'hr.department'

    project_id = fields.Many2one('project.project', string="Project", domain="[('is_aicanvas', '=', True)]")

    def _compute_total_canva_ideas(self):
        for rec in self:
            rec.total_canva_ideas = self.env['project.task'].search_count([
                ('department_id', '=', self.id)
            ])

    total_canva_ideas = fields.Integer(string="Total AI Canvas", compute=_compute_total_canva_ideas)

    def action_view_department_ideas(self):
        action = {
            'name': 'Department Canva Ideas',
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            # #if VERSION >= "18.0"
            'view_mode': 'kanban,list,form',
            # #elif VERSION <= "17.0"
            'view_mode': 'kanban,tree,form',
            # #endif
            'target': 'current',
            'domain': [("department_id", '=', self.id)],
        }
        return action
