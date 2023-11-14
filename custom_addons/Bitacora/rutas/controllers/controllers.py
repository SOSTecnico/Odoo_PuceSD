# -*- coding: utf-8 -*-
# from odoo import http


# class Rutas(http.Controller):
#     @http.route('/rutas/rutas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rutas/rutas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rutas.listing', {
#             'root': '/rutas/rutas',
#             'objects': http.request.env['rutas.rutas'].search([]),
#         })

#     @http.route('/rutas/rutas/objects/<model("rutas.rutas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rutas.object', {
#             'object': obj
#         })
