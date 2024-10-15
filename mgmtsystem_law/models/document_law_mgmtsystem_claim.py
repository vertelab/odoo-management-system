import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class DocumentPageLaw(models.Model):

    _name="document.law.mgmtsystem.claim"
    _description = 'Glue model between document.law and mgmtsystem.claim'

    name = fields.Char(string="Document Law Managementsystem Claim")

    document_law_id = fields.Many2one(comodel_name="document.law")
    mgmtsystem_claim_id = fields.Many2one(comodel_name="mgmtsystem.claim")
