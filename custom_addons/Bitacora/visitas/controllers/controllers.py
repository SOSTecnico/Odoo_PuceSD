# -*- coding: utf-8 -*-
# from odoo import http


# class Visitas(http.Controller):
#     @http.route('/visitas/visitas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

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
