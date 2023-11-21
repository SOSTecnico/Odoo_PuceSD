# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from zk import ZK, const


class Biometricos(http.Controller):

    # API
    @http.route("/api/biometricos", auth='user', type='json')
    def api_biometricos(self, **data):
        biometricos = request.env["biometricos.biometricos"].search_read([])
        return biometricos

    @http.route("/api/biometricos/open", auth='user', type='json')
    def open(self, **data):
        biometrico = request.env["biometricos.biometricos"].search([('id', '=', data['biometrico_id'])])
        zk = ZK(biometrico.ip_address, port=4370, timeout=5, force_udp=True)
        conn = zk.connect()
        conn.unlock(time=3)
        zk.disconnect()
        return {}

    @http.route('/biometricos/dti', auth='user', website=True)
    def open_dti(self, **data):
        if request.env.user.has_group('biometricos.group_user'):
            biometricos = request.env["biometricos.biometricos"].sudo().search(
                ['|', ('name', '=', 'DTI Oficina'), ('name', '=', 'DTI_ESIS')])

            if data:
                bio = biometricos.filtered_domain([('id', '=', int(data['biometrico_id']))])
                zk = ZK(bio.ip_address, port=4370, timeout=5, force_udp=True)

                conn = zk.connect()
                conn.unlock(time=3)
                zk.disconnect()
            return request.render('biometricos.esis_template', {
                'biometricos': biometricos
            })
