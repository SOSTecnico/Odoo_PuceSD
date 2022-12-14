# -*- coding: utf-8 -*-
# from odoo import http


# class Reservaciones(http.Controller):
#     @http.route('/reservaciones/reservaciones', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reservaciones/reservaciones/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('reservaciones.listing', {
#             'root': '/reservaciones/reservaciones',
#             'objects': http.request.env['reservaciones.reservaciones'].search([]),
#         })

#     @http.route('/reservaciones/reservaciones/objects/<model("reservaciones.reservaciones"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reservaciones.object', {
#             'object': obj
#         })
