from odoo import fields, models, api


class Laboratorio(models.Model):
    _name = 'reservas.laboratorios'
    _description = 'Reservas: Laboratorio'

    name = fields.Char(string='Laboratorio', required=True)
    referencia = fields.Char(string='Referencia', required=False)
    capacidad = fields.Integer(string='Capacidad', required=True)

class Programas(models.Model):
    _name = 'reservas.programas'
    _description = 'Reservas: Programa'

    name = fields.Char()

