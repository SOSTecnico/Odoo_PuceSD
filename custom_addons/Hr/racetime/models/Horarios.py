from odoo import fields, models, api
from datetime import timedelta

from odoo.exceptions import ValidationError


class Horarios(models.Model):
    _name = 'racetime.horarios'
    _description = 'Horarios'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(string="Nombre", required=False, tracking=True)
    hora_inicio = fields.Float(string='Hora Inicio', required=True, tracking=True)
    inicio_descanso = fields.Float(string='Inicio Descanso', required=False, tracking=True)
    fin_descanso = fields.Float(string='Fin Descanso', required=False, tracking=True)
    hora_fin = fields.Float(string='Hora Fin', required=True, tracking=True)
    dias = fields.Char(string='Dias', required=False, tracking=True)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True, tracking=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True, tracking=True)
    active = fields.Boolean(string='Active', required=False, default=True, tracking=True)
    empleados_ids = fields.Many2many(comodel_name='hr.employee', string='Empleados')
    tipo = fields.Selection(string='Tipo', required=False, tracking=True,
                            selection=[('principal', 'PRINCIPAL'), ('flexible', 'FLEXIBLE'),
                                       ('cambio_horario', 'CAMBIO DE HORARIO')
                                       ])
