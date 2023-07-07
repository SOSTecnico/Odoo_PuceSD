# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class TransferenciasWeb(http.Controller):
    @http.route('/mis-activos', auth='user', website=True)
    def lista_activos_fijos(self, **kw):
        transferencias = request.env["transferencias.transferencias"].sudo().search(
            [('custodio_destino_id', '=', request.env.user.employee_id.id)], order='codigo desc')

        return request.render('transferencias.lista_activos_template', {
            'page_name': 'activos-fijos',
            'transferencias': transferencias,
            # 'files': files
        })


class ActivosPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        activos = request.env['transferencias.activos'].sudo().search_count(
            [('responsable_id', '=', request.env.user.employee_id.id)])

        values.update({
            'count_activos': activos
        })

        return values
