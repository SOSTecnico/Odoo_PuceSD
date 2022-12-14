# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Escuela(models.Model):
    _name = 'reservaciones.escuelas'
    _description = 'Escuela'

    name = fields.Char(string="Escuela/Carrera", required=True)


