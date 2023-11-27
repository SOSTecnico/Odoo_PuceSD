from odoo import fields, models, api


class reservas(models.Model):
    _name ='reservas.reservaciones'
    _description = 'reservaciones'

    sala = fields.Char(string='Sala')