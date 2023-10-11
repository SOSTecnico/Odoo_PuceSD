# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Visitas(http.Controller):
    @http.route('/api/visitas/check-access/<model("visitas.visitas"):visita>', auth='public', type='json', cors='*',  csrf=False)
    def verificar(self, visita):
        date = visita.valido_hasta.strftime("%Y-%m-%d") if visita.valido_hasta else 0
        info = {
            'estado': visita.estado,
            'visitante': visita.visitante_id.name,
            'valido_hasta': date
        }
        return info

#     @http.route('/visitas/visitas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('visitas.listing', {
#             'root': '/visitas/visitas',
#             'objects': http.request.env['visitas.visitas'].search([]),
#         })

#     @http.route('/visitas/visitas/objects/<model("visitas.visitas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('visitas.object', {
#             'object': obj
#         })
