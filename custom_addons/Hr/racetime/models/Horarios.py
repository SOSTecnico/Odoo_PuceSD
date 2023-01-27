from odoo import fields, models, api


class Horarios(models.Model):
    _name = 'racetime.horarios'
    _description = 'Horarios'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(string="Nombre", required=True, tracking=True)
    hora_inicio = fields.Float(string='Hora Inicio', required=True, tracking=True)
    inicio_descanso = fields.Float(string='Inicio Descanso', required=False, tracking=True)
    fin_descanso = fields.Float(string='Fin Descanso', required=False, tracking=True)
    hora_fin = fields.Float(string='Hora Fin', required=True, tracking=True)
    dias = fields.Char(string='Dias', required=False, tracking=True)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=False)
    fecha_fin = fields.Date(string='Fecha Fin', required=False)
    active = fields.Boolean(string='Active', required=False, default=True)
    empleados_ids = fields.Many2many(comodel_name='hr.employee', string='Empleados')
