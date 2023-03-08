# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class Rolpago(CustomerPortal):
    @http.route('/rolpago/mis_roles', auth='public', website=True)
    def index(self, **kw):
        roles = request.env['rolpago.roles'].sudo().search(
            [('empleado_id', '=', request.env.user.partner_id.employee_ids[0].id)])
        return request.render('rolpago.roles_template', {
            'roles': roles
        })

    @http.route(['/rolpago/roles/<int:rol_id>'], type='http', auth="user", website=True)
    def portal_rol(self, rol_id, access_token=None, report_type=None, download=False, **kw):
        try:
            rol_sudo = self._document_check_access('rolpago.roles', rol_id, access_token)

        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=rol_sudo, report_type=report_type, report_ref='rolpago.action_report_roles',
                                     download=download)
        rol = request.env['rolpago.roles'].browse(rol_id)
        print(rol)

        values = {
            'rol': rol
        }
        return request.render("rolpago.portal_rol_page", values)

    @http.route('/rolpago/cambiar_estado', auth='user', website=True)
    def cambiar_estado(self, **kw):
        id_role = kw['rol_id']

        rol = request.env['rolpago.roles'].sudo().search(
            [('id', '=', id_role)])
        rol.update({
            'estado_rol': kw['estado']
        })
        return request.redirect("/my/home")


class RolesPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        roles = request.env['rolpago.roles'].sudo().search_count(
            [('empleado_id', '=', request.env.user.partner_id.employee_ids[0].id)])

        values.update({
            'count_roles': roles
        })
        return values
