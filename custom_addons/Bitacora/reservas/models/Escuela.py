from odoo import fields, models, api


class escuela(models.Model):
    _name = 'reservas.escuela'
    _description = 'escuela'

    carrera = fields.Char(string='Escuela')

