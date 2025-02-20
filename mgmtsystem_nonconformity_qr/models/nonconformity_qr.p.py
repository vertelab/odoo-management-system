import base64
from io import BytesIO
from odoo import models, fields, api

try:
    import qrcode
except ImportError:
    qrcode = None


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
            rec.url = False
            if rec.id:
            	rec.url = f"{base_url}/nonconformity-qr/{rec.id}"

    url = fields.Char(string="URL", compute=_compute_url)

    def generate_qr_code(self):
        for rec in self:
            allow_qr_code = self.env['ir.config_parameter'].sudo().get_param(
                'mgmtsystem_nonconformity_qr.allow_qr_code', False
            )
            if allow_qr_code:
                qr_code = qrcode.QRCode(
                    version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4
                )
                qr_code.add_data(self.url)
                qr_code.make(fit=True)

                img = qr_code.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered, format="PNG")

                # Encode the image in Base64
                img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                rec.qr_code = img_base64
            else:
                rec.qr_code = False

    qr_code = fields.Binary("QR Code", compute=generate_qr_code)


class Origin(models.Model):
    _inherit = "mgmtsystem.nonconformity.origin"

    nonconformity_qr_id = fields.Many2one("mgmtsystem.nonconformity.qr", string="Nonconformity QR")
