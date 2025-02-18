# Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemConfigSettings(models.TransientModel):
    """This class is used to activate management system Applications."""

    _inherit = "res.config.settings"

    allow_qr_code = fields.Boolean(
        "Nonconformity QR",
        config_parameter='mgmtsystem_nonconformity_qr.allow_qr_code'
    )
