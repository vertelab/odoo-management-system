import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class DocumentPage(models.Model):
    _inherit = 'document.page'
    _description = 'Adds connections to mgmtsystem modules for the document_law module.'

    document_law_ids = fields.One2many(comodel_name="document.law", inverse_name="document_page_manual")
