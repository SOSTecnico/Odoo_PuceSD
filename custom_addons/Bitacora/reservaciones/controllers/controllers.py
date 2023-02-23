# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64
from io import BytesIO
import qrcode
from datetime import  datetime


class Reservaciones(http.Controller):
    @http.route('/laboratorios', auth='public', website=True)
    def formulario_codigos(self, **kw):
        return request.render("reservaciones.generador_codigo_template", {})

    @http.route('/laboratorios/generar_codigo', auth='public', website=True)
    def generador_codigo(self, **data):
        usuario = request.env['reservaciones.usuarios'].sudo().search([('email', '=', data['email'])])
        info = {
            "usuario_id": usuario.id,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "laboratorio": data['laboratorio']
        }
        res = request.env['reservaciones.codigo_qr'].sudo().create(info)
        img = qrcode.make(info)

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        res.update({
            'codigo_qr': base64.b64encode(buffered.getvalue())
        })
        template = request.env.ref('reservaciones.notificacion_qr_template')
        template.send_mail(res.id, force_send=True)
        return self.formulario_codigos()
