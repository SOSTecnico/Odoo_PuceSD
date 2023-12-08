# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Banner(http.Controller):
    @http.route('/banner/check-usuario', auth='public', csrf=False, cors='*', type='json')
    def verificar_datos(self, **data):

        usuario = request.env['banner.usuarios'].sudo().search([('cedula', '=', data['cedula'])])

        if usuario:
            datos = {
                'cedula': usuario.read()[0]['cedula'],
                'nombres': usuario.read()[0]['nombres'],
                'apellidos': usuario.read()[0]['apellidos'],
                'correo': usuario.read()[0]['correo'],
            }
            return datos
        else:
            return {}
