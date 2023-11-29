from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class reservas(models.Model):
    _name = 'reservas.reservaciones'
    _description = 'reservaciones'

    codigo = fields.Char(string='Codigo de Sala')
    sala = fields.Selection(
        string='Sala',
        selection=[('sala computo 1', 'SALA COMPUTO 1'),
                   ('sala computo 2', 'SALA COMPUTO 2'),
                   ('sala computo 3', 'SALA COMPUTO 3'),
                   ('sala computo 5', 'SALA COMPUTO 5'),
                   ('sala computo 6', 'SALA COMPUTO 6'),
                   ('sala computo 7', 'SALA COMPUTO 7'), ], default='sala computo 1')

    responsable = fields.Char(string='Responsable')
    asignatura = fields.Char(string='Asignatura')
    fecha_inicio = fields.Date('Fecha inicio')
    hora_inicio = fields.Datetime('Hora inicio')
    hora_final = fields.Datetime('Hora Final')
    fecha_final = fields.Date('Fecha Final')
