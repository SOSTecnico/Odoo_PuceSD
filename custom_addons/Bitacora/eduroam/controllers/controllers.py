# -*- coding: utf-8 -*-
from oracledb import Error

from odoo import http
from odoo.http import request


class Eduroam(http.Controller):
    @http.route('/eduroam/formulario', auth='user', website=True)
    def index(self, **kw):
        if request.env.user.has_group('eduroam.group_admin'):
            return request.render('eduroam.template_generar_usuario')

    @http.route('/eduroam/generar_usuarios', auth='user', website=True)
    def generar_script(self, **data):
        if not 'cedulas' in data:
            return request.redirect('/eduroam/formulario')

        if request.env.user.has_group('eduroam.group_admin'):
            cedulas = data['cedulas'].split(',')
            UsuariosModel = request.env['eduroam.usuarios']
            try:
                result = UsuariosModel.obtener_usuarios(cedulas)
                pidms = request.env['eduroam.usuarios'].search([]).mapped('pidm')
                for usuario in result:
                    if str(usuario['PIDM']) not in pidms:
                        request.env['eduroam.usuarios'].create({
                            'name': '',
                            'primer_nombre': usuario['PRIMER_NOMBRE'].upper(),
                            'segundo_nombre': usuario['SEGUNDO_NOMBRE'].upper(),
                            'primer_apellido': usuario['APELLIDOS'].split('/')[0].upper(),
                            'segundo_apellido': usuario['APELLIDOS'].split('/')[1].upper(),
                            'password': usuario['CEDULA'],
                            'pidm': usuario['PIDM'],
                            'cedula': usuario['CEDULA'],
                        })
                usuarios = request.env['eduroam.usuarios'].search([('cedula', 'in', cedulas)])

                return request.render('eduroam.template_eduroam_script', {'usuarios': usuarios})
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
