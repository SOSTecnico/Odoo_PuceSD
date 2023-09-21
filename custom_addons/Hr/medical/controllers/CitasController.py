import json

from odoo import http
from odoo.http import request


class CitasController(http.Controller):

    # Vistas
    @http.route('/centro-medico/solicitud-cita', auth="public", website=True)
    def formulario_cedula(self, **data):
        if data:

            cedula = data['cedula']
            user = {
                'nombre': '',
                'cedula': '',
                'correo': ''
            }

            model_empleado = request.env['hr.employee'].sudo()
            model_estudiante = request.env['banner.usuarios'].sudo()

            usuario = model_empleado.search([('identification_id', '=', cedula)])

            if not usuario:
                usuario = model_estudiante.search([('cedula', '=', cedula)])

                if not usuario:
                    return request.render('medical.solicitud_cita_no_user')

                user.update({
                    'nombre': usuario.name,
                    'cedula': usuario.cedula,
                    'correo': usuario.correo
                })
            else:
                user.update({
                    'nombre': usuario.name,
                    'cedula': usuario.identification_id,
                    'correo': usuario.work_email
                })

            return request.render('medical.solicitud_cita_formulario', {'usuario': user})

        return request.render("medical.solicitud_cita_check_usuario")
