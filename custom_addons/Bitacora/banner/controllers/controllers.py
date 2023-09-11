# -*- coding: utf-8 -*-
# from odoo import http


# class Banner(http.Controller):
#     @http.route('/banner/banner', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/banner/banner/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('banner.listing', {
#             'root': '/banner/banner',
#             'objects': http.request.env['banner.banner'].search([]),
#         })

#     @http.route('/banner/banner/objects/<model("banner.banner"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('banner.object', {
#             'object': obj
#         })
