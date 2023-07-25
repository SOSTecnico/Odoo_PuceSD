# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Api(http.Controller):
    @http.route('/api/user-info', auth='user', type='json')
    def user_img(self, **kw):
        user = request.env.user
        user_info = user.read(['avatar_1920','image_128'])[0]

        groups = user.groups_id.get_xml_id()

        return {
            'user_info': user_info,
            'groups': groups
        }

#     @http.route('/api/api/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('api.listing', {
#             'root': '/api/api',
#             'objects': http.request.env['api.api'].search([]),
#         })

#     @http.route('/api/api/objects/<model("api.api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('api.object', {
#             'object': obj
#         })
