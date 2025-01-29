import logging

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class DocumentLaw(models.Model):
    _inherit = 'document.law'

    ai_policy = fields.Text()
        



