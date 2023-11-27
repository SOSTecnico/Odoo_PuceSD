from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class reservas(models.Model):
    _name ='reservas.reservaciones'
    _description = 'reservaciones'

    codigo = fields.Char(string='Codigo de Sala')
    sala = fields.Char(string='Sala')
    responsable = fields.Char(string='Responsable')
    asignatura = fields.Char(string='Asignatura')
    fecha_inicio = fields.Date(string='Fecha inicio')
    hora_inicio = fields.Float(string='Hora inicio')
    hora_final = fields.Float(string='Hora Final')
    fecha_final = fields.Date(string='Fecha Final')

