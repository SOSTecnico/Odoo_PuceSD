# -*- coding: utf-8 -*-
# from odoo import http


# class Aleatoria(http.Controller):
#     @http.route('/aleatoria/aleatoria', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aleatoria/aleatoria/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('aleatoria.listing', {
#             'root': '/aleatoria/aleatoria',
#             'objects': http.request.env['aleatoria.aleatoria'].search([]),
#         })

#     @http.route('/aleatoria/aleatoria/objects/<model("aleatoria.aleatoria"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aleatoria.object', {
#             'object': obj
#         })
