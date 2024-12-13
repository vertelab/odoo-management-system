import base64
from odoo import http, _
from odoo.http import request
from werkzeug.utils import redirect
from werkzeug.urls import url_encode
from odoo.exceptions import AccessError
from werkzeug.exceptions import Forbidden, NotFound


class NonConformity(http.Controller):

    def _process_media(self, media, res_id):
        media_name = media.filename
        # attachment = media.read()
        # print("attachment", attachment)
        attachment_id = request.env['ir.attachment'].sudo().create({
            'name': media_name,
            'res_name': media_name,
            'type': 'binary',
            'res_model': 'mgmtsystem.nonconformity',
            'res_id': res_id,
            'datas': base64.encodebytes(media.read()),
        })
        return attachment_id

    @http.route(['/nonconformity-qr/<int:nonconformity_qr_id>'], type='http', auth="user", website=True)
    def nonconformity_qr(self, nonconformity_qr_id, **kw):
        nonconformity_qr_id = request.env['mgmtsystem.nonconformity.qr'].browse(nonconformity_qr_id).exists()
        if not nonconformity_qr_id:
            raise NotFound("No Record Found")
        self._check_user_impersonification(nonconformity_qr_id=nonconformity_qr_id)

        extra_vals = {}

        if request.httprequest.method == "POST":
            try:
                media = kw.pop('media')
                nonconformity_id = request.env['mgmtsystem.nonconformity'].create({
                    **kw,
                    'origin_ids': nonconformity_qr_id.origin_ids.ids,
                    'user_id': nonconformity_qr_id.responsible_user_id.id,
                    'system_id': nonconformity_qr_id.system_id.id,
                    'manager_user_id': nonconformity_qr_id.manager_user_id.id,
                    'department_id': nonconformity_qr_id.department_id.id,
                    'responsible_user_id': nonconformity_qr_id.responsible_user_id.id,
                    'partner_id': 1,
                })
                self._process_media(media, nonconformity_id.id)
                if nonconformity_id:
                    return redirect('/nonconformity-qr/%s?%s' % (nonconformity_qr_id.id, url_encode({'status': 'success'})))
            except Exception as e:
                return redirect('/nonconformity-qr/%s?%s' % (nonconformity_qr_id.id, url_encode({'status': 'error'})))

        return request.render(
            "mgmtsystem_nonconformity_qr.nonconformity_form_temp",
            {'nonconformity_qr': nonconformity_qr_id, 'extra_vals': extra_vals}
        )

    def _check_user_impersonification(self, nonconformity_qr_id=None):
        if not nonconformity_qr_id:
            raise Forbidden()
        if nonconformity_qr_id.responsible_user_id.id != request.env.uid:
            raise AccessError(_(
                'You are trying to impersonate another user, but this can only be done by the assigned user'
            ))
