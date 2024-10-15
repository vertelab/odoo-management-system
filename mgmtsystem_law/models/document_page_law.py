import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class DocumentPageLaw(models.Model):

    _name="document.page.law"
    _description = 'Glue model between document.page and document.law'

    name = fields.Char(string="Document Page Law")

    document_law_id = fields.Many2one(comodel_name="document.law")
    document_page_id = fields.Many2one(comodel_name="document.page")
