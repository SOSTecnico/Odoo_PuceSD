import json
from datetime import datetime, timedelta
import dateutil.parser
import pytz

from odoo import http
from odoo.http import request


class CitasController(http.Controller):

    @http.route('/medical/check-user', auth='public', type='json', cors='*', csrf=False)
    def check_user(self, **data):
        if data:
            vals = {}
            usuario = request.env['hr.employee'].sudo().search([('identification_id', '=', data['dni'])])
            if not usuario:
                usuario = request.env['banner.usuarios'].sudo().search([('cedula', '=', data['dni'])])
                if not usuario:
                    return {
                        'msg': 'Usuario no existe',
                        'code': 404
                    }
                vals.update({
                    'correo': usuario.correo,
                    'nombre': usuario.name
                })
            else:
                vals.update({
                    'correo': usuario.work_email,
                    'nombre': usuario.name
                })
            return {
                'msg': 'exito',
                'code': 200,
                'result': vals
            }

    @http.route('/medical/get-appointments', auth='public', type='json', cors='*', csrf=False)
    def obtener_citas(self, **data):
        inicio = dateutil.parser.parse(data['start'])
        fin = dateutil.parser.parse(data['end'])
        citas = request.env['medical.citas'].sudo().search_read(
            [('date_start', '>=', inicio), ('date_stop', '<=', fin)])

        return citas

    @http.route('/medical/set-appointment', auth='public', type='json', cors='*', csrf=False)
    def establecer_cita(self, **data):

        model_citas = request.env['medical.citas'].sudo()
        paciente = request.env['medical.paciente'].sudo().search([('name', '=', data['user'])])

        cita = model_citas.create({
            'date_start': data['start'],
            'date_stop': data['end'],
            'paciente': data['user'],
            'paciente_id': paciente or False,
            'name': data['user'],

        })
        print(data['start'])
        print(data['end'])

        template_id = request.env.ref('medical.cita_agendada_email').id
        email = request.env["mail.template"].sudo().browse(template_id)
        email.update({
            'email_to': data['email']
        })
        email.send_mail(cita.id, force_send=True)

        return {
            'msg': 'exito',
            'code': 200,
            'result': cita.read()[0]
        }
