# -*- coding: utf-8 -*-
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo import http
from odoo.http import request

from datetime import datetime, timedelta
import itertools


class Racetime(http.Controller):
    @http.route('/solicitud-permiso', auth='user', website=True)
    def index(self, **kw):
        tipos_permiso = request.env["racetime.tipos_permiso"].search([])
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
            'descripcion': data['descripcion']
        })

        template_id = request.env.ref("racetime.solicitud_permiso_email_template").id
        request.env["mail.template"].browse(template_id).send_mail(res.id, force_send=True)

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

    # Marcaciones
    @http.route(['/mis-marcaciones', '/mis-marcaciones/page/<int:page>'], auth='user', website=True)
    def marcaciones(self, page=1, sortby='fecha', search='', search_in='all', **kw):
        obj_m = request.env["racetime.detalle_marcacion"].sudo()
        total = obj_m.search_count([("empleado_id", "=", request.env.user.employee_id.id)])

        page_detail = pager(url='/mis-marcaciones',
                            total=total,
                            page=page,
                            url_args={'sortby': sortby, 'search_in': search_in, 'search': search},
                            step=15)

        sorted_list = {
            'fecha': {
                'label': 'Fecha',
                'order': 'fecha_hora desc'
            },
        }

        search_list = {
            'all': {'label': 'Todo', 'input': 'all', 'domain': [("empleado_id", "=", request.env.user.employee_id.id)]},
            'fecha_hora': {'label': 'Fecha', 'input': 'fecha_hora',
                           'domain': [("empleado_id", "=", request.env.user.employee_id.id),
                                      ('fecha_hora', '>=', search), ('fecha_hora', '<=', search)]}
        }

        search_domain = search_list[search_in]['domain']

        # default_order_by = sorted_list[sortby]['order']

        marcaciones = obj_m.search(search_domain, order='fecha_hora desc', limit=15, offset=page_detail['offset'])

        marc = []

        for m in marcaciones:
            marc.append({
                'fecha': m.fecha_hora.strftime('%Y-%m-%d'),
                'hora': (m.fecha_hora - timedelta(hours=5)).strftime("%H:%M:%S")
            })

        values = {
            'marcaciones': marc,
            'page_name': 'mis-marcaciones',
            'pager': page_detail,
            'sortby': sortby,
            # 'searchbar_sortings': sorted_list,
            'search': search,
            'searchbar_inputs': search_list,
            'search_in': search_in
        }
        return request.render("racetime.lista_marcaciones_template", values)

        # API

    @http.route('/racetime/api/marcaciones', auth='user', type='json')
    def api_marcaciones(self, **data):
        fecha_inicio = data['dates']['startDate']
        fecha_fin = data['dates']['endDate']

        marcaciones = request.env['racetime.detalle_marcacion'].sudo().search_read(
            [('empleado_id', '=', request.env.user.employee_id.id), ('fecha_hora', '>=', fecha_inicio),
             ('fecha_hora', '<=', fecha_fin)], order='fecha_hora desc')

        key_func = lambda self: self['fecha_hora'].strftime('%Y-%m-%d')
        marcaciones_agrupadas = []
        for key, group in itertools.groupby(marcaciones, key_func):
            marcaciones_agrupadas.append({
                'fecha': key,
                'records': list(group)[::-1]
            })

        return marcaciones_agrupadas


class PermisosPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        user = request.env.user
        permisos = request.env['racetime.permisos'].sudo().search_count(
            [('empleado_id', '=', user.employee_id.id)])

        marcaciones = request.env['racetime.detalle_marcacion'].sudo().search_count(
            [('empleado_id', '=', user.employee_id.id)])

        values.update({
            'count_permisos': permisos,
            'count_marcaciones': marcaciones
        })

        return values
