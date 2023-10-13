import json

from odoo import http
from odoo.http import request
import base64
from datetime import timedelta


class PermisosController(http.Controller):

    @http.route('/solicitud-permiso', auth='user', website=True)
    def index(self, **kw):
        tipos_permiso = request.env["racetime.tipos_permiso"].sudo().search(
            [('name', '!=', 'MÉDICO'), ('name', '!=', 'CARGO A VACACIONES'),
             ('name', '!=', 'RECUPERACION CLASE TP'), ('name', '!=', 'RECUPERACIÓN HORAS'),
             ('name', '!=', 'DIAS DE ANTIGÜEDAD')])

        return request.render('racetime.solicitud_permiso_template', {
            'user': request.env.user,
            'tipos_permiso': tipos_permiso
        })

    @http.route('/agendar-permiso', auth='user', method='POST', website=True)
    def agendar_permiso(self, **data):
        jefe_inmediato = request.env["hr.employee"].sudo().search([("work_email", '=', data['email_jefe'])])

        aprobado_por = [(4, jefe_inmediato.id)] if jefe_inmediato else False

        res = request.env["racetime.permisos"].sudo().create({
            'estado': 'pendiente',
            'empleado_id': request.env.user.employee_id.id,
            'aprobado_por_id': aprobado_por,
            'desde_fecha': data['fecha_inicio'],
            'hasta_fecha': data['fecha_fin'],
            'desde_hora': self.string_to_time(data["hora_inicio"]),
            'hasta_hora': self.string_to_time(data["hora_fin"]),
            'tipo_permiso_id': int(data['tipo_permiso_id']),
            'todo_el_dia': True if 'todo_el_dia' in data else False,
            'descripcion': data['descripcion'],
            'adjunto': base64.b64encode(data.get('adjunto').read()) or False
        })

        template_id = request.env.ref("racetime.solicitud_permiso_email_template").id
        email = request.env["mail.template"].sudo().browse(template_id)
        if 'email_cc' in data and data['email_cc']:
            emails = []
            for e in data['email_cc'].split(','):
                emails.append(e.strip())

            email.update({
                'email_cc': ','.join(emails)
            })

        request.env["mail.template"].sudo().browse(template_id).send_mail(res.id, force_send=True)

        return self.solicitud_registrada()

    def string_to_time(self, string_time):
        if not string_time:
            string_time = "00:00"
        h, m = string_time.split(":")
        return timedelta(hours=int(h), minutes=int(m)).total_seconds() / 60 / 60

    @http.route('/mis-permisos', auth='user', website=True)
    def lista_de_permisos(self):
        permisos = request.env["racetime.permisos"].sudo().search(
            [("empleado_id", "=", request.env.user.employee_id.id)], order="desde_fecha desc")

        return request.render("racetime.lista_permisos_template", {"permisos": permisos, 'page_name': 'mis-permisos'})

    @http.route("/solicitud-registrada", auth="user", website=True)
    def solicitud_registrada(self):
        return request.render("racetime.solicitud_permiso_registrada_template")

    @http.route("/permisos/aprobar", auth='public', csrf=False, website=True)
    def aprobar_permiso(self, **data):
        if data:
            permiso = request.env['racetime.permisos'].sudo().search([('id', '=', data.get('permiso_id'))])
            if permiso:
                if permiso.estado == 'pendiente':
                    status = data.get('estado')

                    template_id = request.env.ref("racetime.respuesta_permiso_email_template").id
                    email = request.env["mail.template"].sudo().browse(template_id)
                    permiso.update({
                        'estado': status
                    })

                    if data.get('estado') == 'aprobado':
                        if permiso.tipo_permiso_id.name == 'CITA MÉDICA' or permiso.tipo_permiso_id.name == 'REPOSO MÉDICO':
                            emails_cc = []
                            for e in email.email_cc.split(","):
                                emails_cc.append(e.strip())

                            emails_cc.append("cmedico@pucesd.edu.ec")
                            emails_cc.append("cmedicoa@pucesd.edu.ec")

                            email.update({
                                'email_cc': emails_cc
                            })

                    email.send_mail(permiso.id, force_send=True)

                    return request.render("racetime.solicitud_permiso_registrada_jefe_template", {
                        'status': 200
                    })
                else:
                    return request.render("racetime.solicitud_permiso_registrada_jefe_template", {
                        'status': 500,
                        'msg': 'No se puede modificar el permiso'
                    })
            else:
                return request.render("racetime.solicitud_permiso_registrada_jefe_template", {
                    'status': 404,
                    'msg': 'No se puede modificar el permiso'
                })
