from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _description = 'scaffold_test.scaffold_test'
    _inherit = 'document.law'

    ai_summary = fields.Text(store=True)

    def create_ai_summary(self):
        pass

