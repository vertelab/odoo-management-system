from odoo import models, fields, api


class NonConformityQR(models.Model):
    _name = "mgmtsystem.nonconformity.qr"
    _description = "Nonconformity QR"

    system_id = fields.Many2one("mgmtsystem.system", string="System")
    department_id = fields.Many2one("hr.department", string="Department")
    origin_ids = fields.One2many("mgmtsystem.nonconformity.origin", "nonconformity_qr_id", string="Origins")
    responsible_user_id = fields.Many2one("res.users", string="Responsible")
    manager_user_id = fields.Many2one("res.users", string="Manager")

    def _compute_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            rec.url = f"{base_url}/nonconformity-qr/{rec.id}"

    url = fields.Char(string="URL", compute=_compute_url)


class Origin(models.Model):
    _inherit = "mgmtsystem.nonconformity.origin"

    nonconformity_qr_id = fields.Many2one("mgmtsystem.nonconformity.qr", string="Nonconformity QR")

