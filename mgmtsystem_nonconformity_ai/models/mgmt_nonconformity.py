from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class MgmtsystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    ai_quest_id = fields.Many2one(comodel_name='ai.quest', string="AI Quest", help="")

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        if not self.stage_id.state == "done":
            if self.ai_quest_id:
                self.ai_quest_id.status = 'active'
                self.ai_quest_id.channel_id.write({'active': True,})
        else:
            if self.ai_quest_id.channel_id:
                self.ai_quest_id.status = 'done'
                self.ai_quest_id.channel_id.write({'active': False})


    @api.onchange("name", "ref")
    def _onchange_name(self):
        if self.ai_quest_id:
            self.ai_quest_id.write({'name': f"[{self.ref}] {self.name}"})
            if self.ai_quest_id.channel_id:
                self.ai_quest_id.channel_id.write({'name': f"[{self.ref}] {self.name}"})
            
 
    @api.model
    def create(self, vals):
        mgmtsystem_nonconformity = super(MgmtsystemNonconformity, self).create(vals)
        action_plan_stage = self.env.ref('mgmtsystem_nonconformity.stage_pending')
        if self.stage_id.id == action_plan_stage.id:
            if not mgmtsystem_nonconformity.ai_quest_id:
                mgmtsystem_nonconformity.ai_quest_id = self.env['ai.quest'].create({
                    'name': f"[{mgmtsystem_nonconformity.ref}] {mgmtsystem_nonconformity.name}",
                    'ai_type': 'nonconformity-chat',
                    'init_type': 'channel',
                    'status': 'active',
                    'code': """
record = env["mgmtsystem.nonconformity"].search([('ai_quest_id','=',quest.id)])
result = quest.build(session=session,message=message_body,record=record).invoke(message_invoke)
                    """,
                })
                self.env['ai.quest.agent'].create({
                    'ai_agent_id': self.env.ref('mgmtsystem_nonconformity_ai.ai_agent_nonconformity_chat').id,
                    'ai_quest_id': mgmtsystem_nonconformity.ai_quest_id.id
                })
                mgmtsystem_nonconformity.ai_quest_id.channel_id.create({
                    'name': f"[{mgmtsystem_nonconformity.ref}] {mgmtsystem_nonconformity.name}",
                    'ai_quest_id': mgmtsystem_nonconformity.ai_qu_model_memory_type_dataest_id.id,
                    'description': _('Chat with Management System Nonconformity'),
                })
        return mgmtsystem_nonconformity

            
    def write(self, vals):
        result = super(MgmtsystemNonconformity, self).write(vals)
        for mgmtsystem_nonconformity in self:
            action_plan_stage = self.env.ref('mgmtsystem_nonconformity.stage_pending')
            if mgmtsystem_nonconformity.stage_id.id == action_plan_stage.id:
                if not mgmtsystem_nonconformity.ai_quest_id:
                    mgmtsystem_nonconformity.ai_quest_id = self.env['ai.quest'].create({
                        'name': f"[{mgmtsystem_nonconformity.ref}] {mgmtsystem_nonconformity.name}",
                        'ai_type': 'nonconformity-chat',
                        'init_type': 'channel',
                        'status': 'active',
                        'ai_agent_ids': [(
                            0, 0, {'ai_agent_id': self.env.ref('mgmtsystem_nonconformity_ai.ai_agent_nonconformity_chat').id}
                        )],
                        'code': """
record = env["mgmtsystem.nonconformity"].search([('ai_quest_id','=',quest.id)])
result = quest.build(session=session,message=message_body,record=record).invoke(message_invoke)
                        """,
                        'description': _('Chat with Management System Nonconformity'),
                    })
                    channel_model = 'mail.channel'
                    mgmtsystem_nonconformity.ai_quest_id.channel_id = self.env[channel_model].create({
                        'name': f"[{mgmtsystem_nonconformity.ref}] {mgmtsystem_nonconformity.name}",
                        'ai_quest_id': mgmtsystem_nonconformity.ai_quest_id.id,
                        'description': _('Chat with Management System Nonconformity'),
                    }).id
        return result


