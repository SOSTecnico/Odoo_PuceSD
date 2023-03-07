# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import json


class Rubros(models.Model):
    _name = "rolpago.rubros"
    _description = "rubros"

    valor = fields.Float(string='Valor del rubro', digits=(6, 2))

    tipo_rubro_id = fields.Many2one(comodel_name='rolpago.tipo_rubro', string='Rubro', required=False)

    horas_laborables = fields.Float(string='Horas laborales', required=False)

    roles_id = fields.Many2one(comodel_name='rolpago.roles', string='Rol', required=True, ondelete='cascade')

class TipoRubro(models.Model):
    _name = 'rolpago.tipo_rubro'
    _description = 'TipoRubro'

    name = fields.Char(string="Nombre")
    tipo = fields.Selection(string='Tipo', selection=[('I', 'INGRESO'), ('D', 'DESCUENTO'), ('P', 'P')],
                            required=False, )
    aplica = fields.Selection(string='Aplica', selection=[('SI', 'Sí'), ('NO', 'No'), ], required=False, )
    imponible = fields.Selection(string='Imponible', selection=[('S', 'Sí'), ('N', 'No'), ], required=False, )