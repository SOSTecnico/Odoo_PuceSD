# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Visitas(http.Controller):
    @http.route('/visitas/verificar', auth='public', type='json')
    def verificar(self, **data):
        if data:
            model = request.env['visitas.visitas'].sudo()
            record = model.browse(data['id'])
            values = {
                'access': 0
            }
            if record:
                rec = record.read()[0]
                receptor = record.receptor_id.read(['name']) or ''
                values.update({
                    'visitante': rec['name'],
                    'receptor': receptor
                })

                if record.estado == 'valido':
                    values.update({'access': 1})
                    return values

        return False

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
