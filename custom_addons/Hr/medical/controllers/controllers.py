# -*- coding: utf-8 -*-
# from odoo import http


# class Medical(http.Controller):
#     @http.route('/medical/medical', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/medical/medical/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('medical.listing', {
#             'root': '/medical/medical',
#             'objects': http.request.env['medical.medical'].search([]),
#         })

#     @http.route('/medical/medical/objects/<model("medical.medical"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('medical.object', {
#             'object': obj
#         })
