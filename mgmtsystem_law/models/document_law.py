import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class DocumentLaw(models.Model):
    _inherit = 'document.law'
    _description = 'Adds connections to mgmtsystem modules for the document_law module.'

    mgmtsystem_claim_ids = fields.Many2many(comodel_name='mgmtsystem.claim', string="Claims")
    mgmtsystem_action_ids = fields.Many2many(comodel_name="mgmtsystem.action", string="Actions")
    document_page_ids = fields.Many2many(comodel_name="document.page", string="Document Pages")
    mgmtsystem_hazard_ids = fields.Many2many(comodel_name="mgmtsystem.hazard", string="Hazards")
    
    system_id = fields.Many2one(comodel_name="mgmtsystem.system", string="System")