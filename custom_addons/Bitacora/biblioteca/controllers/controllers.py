# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request

class Biblioteca(http.Controller):
    @http.route('/biblioteca/usuarios', auth='public')
    def index(self, **kw):
        usuarios = request.env['biblioteca.usuarios'].search([])
        return json.load(usuarios)

#     @http.route('/biblioteca/biblioteca/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('biblioteca.listing', {
#             'root': '/biblioteca/biblioteca',
#             'objects': http.request.env['biblioteca.biblioteca'].search([]),
#         })

#     @http.route('/biblioteca/biblioteca/objects/<model("biblioteca.biblioteca"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('biblioteca.object', {
#             'object': obj
#         })
