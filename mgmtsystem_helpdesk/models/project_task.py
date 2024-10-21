from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):

    _inherit = "project.task"
    _description = 'Creates ESRS datapoints'

    claims_ids = fields.One2many(comodel_name="mgmtsystem.claim", inverse_name="project_task_id")
    claims_count = fields.Integer(compute="_compute_claims_count")

    nonconformity_ids = fields.One2many(comodel_name="mgmtsystem.nonconformity", inverse_name="project_task_id")
    nonconformity_count = fields.Integer(compute="_compute_nonconformity_count")

    def claims_tree_view(self):
        
        return {
            "name": "Claims",
            "type": "ir.actions.act_window",
            "res_model": "mgmtsystem.claim",
            "views": [[False, "tree"] if self.claims_count else [False, "form"]],
            "domain": [("project_task_id", "=", self.id)],
            "context": { "default_project_task_id": self.id }
        }
    
    def nonconformity_tree_view(self):
    
        return {
            "name": "Nonconformitys",
            "type": "ir.actions.act_window",
            "res_model": "mgmtsystem.nonconformity",
            "views": [[False, "kanban"], [False, "form"] ],
            "domain": [("project_task_id", "=", self.id)],
            "context": { "default_project_task_id": self.id }
        }
    
    def _compute_claims_count(self):

        self.claims_count = len(self.claims_ids)

    def _compute_nonconformity_count(self):

        self.nonconformity_count = len(self.nonconformity_ids)