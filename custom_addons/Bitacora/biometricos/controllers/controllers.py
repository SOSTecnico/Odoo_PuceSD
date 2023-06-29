# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from zk import ZK, const


class Biometricos(http.Controller):

    @http.route('/biometricos/biometricos', auth='user', website=True)
    def index(self, **kw):
        biometricos = request.env["biometricos.biometricos"].sudo().search([])
        return request.render("biometricos.list_biometricos", {
            "biometricos":biometricos
        })

    @http.route("/biometricos/open", auth='user')
    def open(self, **data):
        biometrico = request.env["biometricos.biometricos"].search([('id','=',data['biometrico_id'])])
        zk = ZK(biometrico.ip_address, port=4370, timeout=5, force_udp=True)
        conn = zk.connect()
        conn.unlock()
