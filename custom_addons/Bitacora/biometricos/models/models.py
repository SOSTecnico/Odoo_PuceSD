# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Biometricos(models.Model):
    _name = 'biometricos.biometricos'
    _description = 'Biométrico'


    name = fields.Char(string='Nombre', required=True)
    ip_address = fields.Char(string='Dirección IP', required=True)

