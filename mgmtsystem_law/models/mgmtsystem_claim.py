import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class MgmtsystemClaim(models.Model):

    _inherit="mgmtsystem.claim"
    _description = 'Adds connection to document.law from mgmtsystem.claim through document.law.mgmtsystem.claim glue model'

    document_law_ids = fields.One2many(comodel_name="document.law.mgmtsystem.claim", inverse_name="mgmtsystem_claim_id")
