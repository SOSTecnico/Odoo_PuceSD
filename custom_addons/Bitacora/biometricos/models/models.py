# -*- coding: utf-8 -*-

from odoo import models, fields, api
from zk import ZK, const

class Biometricos(models.Model):
    _name = 'biometricos.biometricos'
    _description = 'Biométrico'


    name = fields.Char(string='Nombre', required=True)
    ip_address = fields.Char(string='Dirección IP', required=True)


    def open(self):
        zk = ZK(self.ip_address, port=4370, timeout=5, force_udp=True)
        conn = zk.connect()
        conn.unlock()