# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import qrcode
from io import BytesIO
import base64


class Banner(http.Controller):
    @http.route('/banner/check-usuario', auth='public', csrf=False, cors='*', type='json')
    def verificar_datos(self, **data):

        usuario = request.env['biblioteca.usuarios'].sudo().search([('cedula', '=', data['cedula'])])

        if usuario:

            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
            info = {
                'cedula': usuario.read()[0]['cedula'],
                'nombres': usuario.read()[0]['nombres'],
                'apellidos': usuario.read()[0]['apellidos'],
                'correo': usuario.read()[0]['correo'],
            }

            qr.add_data(info)
            qr.make(fit=True)
            temp = BytesIO()
            img = qr.make_image()
            img.save(temp)
            info.update({
                "image": base64.b64encode(temp.getvalue())
            })
            return info
        else:
            return {}
