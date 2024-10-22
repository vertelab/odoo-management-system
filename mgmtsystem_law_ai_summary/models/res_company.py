from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _description = 'scaffold_test.scaffold_test'
    _inherit = 'res.company'

    ai_company_context = fields.Text(string="Ai Company Context")