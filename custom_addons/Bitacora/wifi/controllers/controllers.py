# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Wifi(http.Controller):
    @http.route('/wifi/tree/estudiantes', auth='user', type="json")
    def index(self, **kw):
        request.env['wifi.estudiantes'].recuperar_usuarios_desde_radius()
        return {"html": ""}

#     @http.route('/wifi/wifi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wifi.listing', {
#             'root': '/wifi/wifi',
#             'objects': http.request.env['wifi.wifi'].search([]),
#         })

#     @http.route('/wifi/wifi/objects/<model("wifi.wifi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wifi.object', {
#             'object': obj
#         })
