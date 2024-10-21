from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class MgmtSystemnonConformity(models.Model):

    _inherit = "mgmtsystem.nonconformity"
    _description = 'Creates ESRS datapoints'

    project_task_id = fields.Many2one(comodel_name="project.task")