# -*- coding: utf-8 -*-
# from odoo import http


# class Transferencias(http.Controller):
#     @http.route('/transferencias/transferencias', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/transferencias/transferencias/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('transferencias.listing', {
#             'root': '/transferencias/transferencias',
#             'objects': http.request.env['transferencias.transferencias'].search([]),
#         })

#     @http.route('/transferencias/transferencias/objects/<model("transferencias.transferencias"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('transferencias.object', {
#             'object': obj
#         })
