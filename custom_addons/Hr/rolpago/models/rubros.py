# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import json


class Rubros(models.Model):
    _name = "rolpago.rubros"
    _description = "rubros"

    descripcion_rubros = fields.Many2one(
        comodel_name='rolpago.descripcion_rubros',
        string='Descripción Rubros',
        required=False)

    valor = fields.Float(string='Valor del rubro', digits=(6, 2))
    horas_laborables = fields.Float(
        string='Horas laborales',
        required=False)

    roles_id = fields.Many2one(
        comodel_name='rolpago.roles',
        string='Roles_id',
        required=False)