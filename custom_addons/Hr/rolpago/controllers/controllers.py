# -*- coding: utf-8 -*-
# from odoo import http


# class Rolpago(http.Controller):
#     @http.route('/rolpago/rolpago', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rolpago/rolpago/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rolpago.listing', {
#             'root': '/rolpago/rolpago',
#             'objects': http.request.env['rolpago.rolpago'].search([]),
#         })

#     @http.route('/rolpago/rolpago/objects/<model("rolpago.rolpago"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rolpago.object', {
#             'object': obj
#         })
