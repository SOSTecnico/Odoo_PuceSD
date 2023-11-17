# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Enfermeria(http.Controller):
    @http.route('/enfermeria/formulario-asistencia', auth='public', website=True)
    def formulario(self, **data):
        print(data)
        if 'cedula' in data:
            usuario = request.env['estudiantes.estudiantes'].sudo().search([('cedula', '=', data['cedula'])])
            carreras = request.env['enfermeria.carreras'].sudo().search([])

            asignaturas = request.env['enfermeria.asignaturas'].sudo().search([])
            laboratorios = request.env['enfermeria.laboratorios'].sudo().search([])

            return request.render('enfermeria.formulario_asistencia_template', {
                'usuario': usuario,
                'carreras': carreras,
                'asignaturas': asignaturas,
                'laboratorios': laboratorios
            })
        return self.formulario_verificar()

    @http.route('/enfermeria/formulario-asistencia/verificar', auth='public', website=True)
    def formulario_verificar(self, **kw):
        return request.render('enfermeria.formulario_asistencia_verificar_template')

#     @http.route('/enfermeria/enfermeria/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('enfermeria.listing', {
#             'root': '/enfermeria/enfermeria',
#             'objects': http.request.env['enfermeria.enfermeria'].search([]),
#         })

#     @http.route('/enfermeria/enfermeria/objects/<model("enfermeria.enfermeria"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('enfermeria.object', {
#             'object': obj
#         })
