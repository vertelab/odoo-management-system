from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class DocumentLaw(models.Model):
    _inherit = "document.law"

    ai_quest_id = fields.Many2one(comodel_name='ai.quest',string="",help="")

    @api.onchange("stage")
    def _onchange_stage_id(self):
        if not self.stage not in ['draft', 'cancel', 'done']:
            if self.ai_quest_id:
                self.ai_quest_id.status = 'active'
                self.ai_quest_id.channel_id.write({'active': True,})
        else:
            if self.ai_quest_id.channel_id:
                self.ai_quest_id.status = 'done'
                self.ai_quest_id.channel_id.write({'active': False})


    @api.onchange("rss_titel")
    def _onchange_name(self):
        if self.ai_quest_id:
            self.ai_quest_id.write({'name': f"{self.rss_titel[:20]}"})
            if self.ai_quest_id.channel_id:
                self.ai_quest_id.channel_id.write({'name': f"{self.rss_titel[:20]}"})


            
    def write(self, vals):
        result = super(DocumentLaw, self).write(vals)
        for ticket in self:
            if not self.stage not in ['draft', 'cancel', 'done']:
                if not ticket.ai_quest_id:
                    ticket.ai_quest_id = self.env['ai.quest'].create({
                        'name': f"{self.rss_titel[:20]}",
                        'sub_description': f"{self.rss_titel}",
                        'ai_type': 'mgmt-law-chat',
                        'init_type': 'channel',
                        'status': 'active',
                        'ai_agent_ids': [(
                            0, 0, {'ai_agent_id': self.env.ref('mgmtsystem_law_ai_chat.ai_agent_mgmt_law_chat').id}
                        )],
                        'code': """result = quest.build(session=session,message=message_body).invoke(message_invoke)""",
                        'description': 'Answer my questions {message}',
                    })

                    ticket.ai_quest_id.channel_id = self.env['discuss.channel'].create({
                        'name': f"{self.rss_titel[:20]}",
                        'ai_quest_id': ticket.ai_quest_id.id,
                        'description': f"{self.rss_titel}",
                    }).id
        return result


