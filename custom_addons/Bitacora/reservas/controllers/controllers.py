# -*- coding: utf-8 -*-
# from odoo import http


# class Reservas(http.Controller):
#     @http.route('/reservas/reservas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reservas/reservas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('reservas.listing', {
#             'root': '/reservas/reservas',
#             'objects': http.request.env['reservas.reservas'].search([]),
#         })

#     @http.route('/reservas/reservas/objects/<model("reservas.reservas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reservas.object', {
#             'object': obj
#         })
