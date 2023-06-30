# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Racetime(http.Controller):
    @http.route('/solicitud-permiso', auth='public', website=True)
    def index(self, **kw):

        return request.render('racetime.solicitud_permiso_template',{
            'user':request.env.user
        })

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
