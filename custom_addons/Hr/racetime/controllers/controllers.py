# -*- coding: utf-8 -*-
# from odoo import http


# class Racetime(http.Controller):
#     @http.route('/racetime/racetime', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/racetime/racetime/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('racetime.listing', {
#             'root': '/racetime/racetime',
#             'objects': http.request.env['racetime.racetime'].search([]),
#         })

#     @http.route('/racetime/racetime/objects/<model("racetime.racetime"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('racetime.object', {
#             'object': obj
#         })
