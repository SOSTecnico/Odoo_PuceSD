# -*- coding: utf-8 -*-
from oracledb import Error

from odoo import http
from odoo.http import request


class Wifi(http.Controller):
    @http.route('/wifi/formulario', auth='user', website=True)
    def index(self, **kw):
        if request.env.user.has_group('wifi.group_admin'):
            return request.render('wifi.template_generar_usuario')
        else:
            return request.redirect('/')

    @http.route('/wifi/generar_usuarios', auth='user', website=True)
    def generar_script(self, **data):
        if not 'cedulas' in data:
            return request.redirect('/wifi/formulario')

        if request.env.user.has_group('wifi.group_admin'):
            cedulas = data['cedulas'].split(',')
            UsuariosModel = request.env['wifi.docentes']
            try:
                result = UsuariosModel.obtener_usuarios(cedulas)
                pidms = request.env['wifi.docentes'].search([]).mapped('pidm')
                for usuario in result:
                    if str(usuario['PIDM']) not in pidms:
                        request.env['wifi.docentes'].create({
                            'name': '',
                            'primer_nombre': usuario['PRIMER_NOMBRE'].upper(),
                            'segundo_nombre': usuario['SEGUNDO_NOMBRE'].upper(),
                            'primer_apellido': usuario['APELLIDOS'].split('/')[0].upper(),
                            'segundo_apellido': usuario['APELLIDOS'].split('/')[1].upper(),
                            'password': usuario['CEDULA'],
                            'pidm': usuario['PIDM'],
                            'cedula': usuario['CEDULA'],
                        })
                usuarios = request.env['wifi.docentes'].search([('cedula', 'in', cedulas)])

                return request.render('wifi.template_docentes_script', {'usuarios': usuarios})
            except Error:
                return request.render('wifi.template_generar_usuario',
                                      {'error': 'Ocurrió un Error, favor comuníquese con el Desarrollador',
                                       'message': Error})
