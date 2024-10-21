from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class MgmtSystemClaim(models.Model):

    _inherit = "mgmtsystem.claim"
    _description = 'Creates ESRS datapoints'

    project_task_id = fields.Many2one(comodel_name="project.task")