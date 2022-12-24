# -*- coding: utf-8 -*-
from oracledb import Error

from odoo import http
from odoo.http import request


class Eduroam(http.Controller):
    @http.route('/eduroam/formulario', auth='user', website=True)
    def index(self, **kw):
        if request.env.user.has_group('eduroam.group_admin'):
            return request.render('eduroam.template_generar_usuario')

    @http.route('/eduroam/generar_usuarios', method=['POST'], auth='user', website=True)
    def generar_script(self, **data):
        if request.env.user.has_group('eduroam.group_admin'):
            cedulas = data['cedulas'].split(',')
            UsuariosModel = request.env['eduroam.usuarios']
            try:
                result = UsuariosModel.obtener_usuarios(cedulas)
                print(result)
                return request.render('eduroam.template_eduroam_script', {'usuarios': result})
            except Error:
                return request.render('eduroam.template_generar_usuario',
                                      {'error': 'Ocurrió un Error, favor comuníquese con el Desarrollador',
                                       'message': Error})

#     @http.route('/eduroam/eduroam/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eduroam.listing', {
#             'root': '/eduroam/eduroam',
#             'objects': http.request.env['eduroam.eduroam'].search([]),
#         })

#     @http.route('/eduroam/eduroam/objects/<model("eduroam.eduroam"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eduroam.object', {
#             'object': obj
#         })
