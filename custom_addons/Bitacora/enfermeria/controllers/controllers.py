# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Enfermeria(http.Controller):
    @http.route('/enfermeria/formulario-asistencia', auth='public', website=True)
    def formulario(self, **kw):
        return request.render('enfermeria.formulario_asistencia_template')

#     @http.route('/enfermeria/enfermeria/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('enfermeria.listing', {
#             'root': '/enfermeria/enfermeria',
#             'objects': http.request.env['enfermeria.enfermeria'].search([]),
#         })

#     @http.route('/enfermeria/enfermeria/objects/<model("enfermeria.enfermeria"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('enfermeria.object', {
#             'object': obj
#         })
