from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class MgmtsystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    ai_coworker_id = fields.Many2one(
        'ai.coworker', string="AI Coworker", help="Per-avvikelse-chatt")

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        if not self.stage_id.state == "done":
            if self.ai_coworker_id:
                self.ai_coworker_id.status = 'active'
                self.ai_coworker_id.channel_id.write({'active': True})
        else:
            if self.ai_coworker_id and self.ai_coworker_id.channel_id:
                self.ai_coworker_id.status = 'done'
                self.ai_coworker_id.channel_id.write({'active': False})

    @api.onchange("name", "ref")
    def _onchange_name(self):
        if self.ai_coworker_id:
            self.ai_coworker_id.write({'name': f"[{self.ref}] {self.name}"})
            if self.ai_coworker_id.channel_id:
                self.ai_coworker_id.channel_id.write(
                    {'name': f"[{self.ref}] {self.name}"})

    def create(self, vals):
        record = super(MgmtsystemNonconformity, self).create(vals)
        record._ensure_nonconformity_coworker()
        return record

    def write(self, vals):
        result = super(MgmtsystemNonconformity, self).write(vals)
        for rec in self:
            rec._ensure_nonconformity_coworker()
        return result

    def _ensure_nonconformity_coworker(self):
        """Skapa per-avvikelse-coworker (channel-init) om den saknas."""
        self.ensure_one()
        if self.ai_coworker_id:
            return
        coworker = self.env['ai.coworker'].create({
            'name': f"[{self.ref}] {self.name}",
            'init_type': 'channel',
            'status': 'active',
            'description': _('Chat with Management System Nonconformity'),
        })
        self.ai_coworker_id = coworker
        if not coworker.channel_id:
            channel = self.env['discuss.channel'].create({
                'name': f"[{self.ref}] {self.name}",
                'description': _('Chat with Management System Nonconformity'),
            })
            coworker.channel_id = channel
        return coworker
