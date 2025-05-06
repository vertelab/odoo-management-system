import logging

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class DocumentLaw(models.Model):
    _inherit = 'document.law'

    law_summary = fields.Html()

    def ai_summary(self):
        quest_ids = self.env["ai.quest"].search([('ai_type', '=', 'law_summary'),('status','=','active')])
        for quest in quest_ids:
            records = self.search([('law_summary', '=', False,),('company_id', '=', quest.company_id.id)],limit=1)
            quest.run(records=records)

        



