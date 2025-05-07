from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class DocumentLaw(models.Model):
    _inherit = "document.law"

    ai_quest_id = fields.Many2one(comodel_name='ai.quest',string="",help="")



