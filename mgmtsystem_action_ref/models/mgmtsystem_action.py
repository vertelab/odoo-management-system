from datetime import datetime, timedelta

from odoo import api, exceptions, fields, models


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    res_ref = fields.Reference(
        copy=False,
        help='The record this action is attached to.',
        selection='_selection_target_model',
        string='Resource Reference',
    )

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]



