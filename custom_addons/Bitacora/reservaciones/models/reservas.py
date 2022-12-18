from odoo import fields, models, api


class Reserva(models.Model):
    _name = 'reservaciones.reservas'
    _description = 'Reserva'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'codigo'

    codigo = fields.Char(string="Código de Reserva")
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True, tracking=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=False, tracking=True)
    hora_inicio = fields.Float(string='Hora Inicio', required=True, tracking=True)
    hora_fin = fields.Float(string='Hora Fin', required=True, tracking=True)
    responsable_id = fields.Many2one(comodel_name='hr.employee', string='Responsable', required=True, tracking=True)
    escuela_id = fields.Many2one(comodel_name='reservaciones.escuelas', string='Escuela', required=False, tracking=True)
    recurso_id = fields.Many2one(comodel_name='reservaciones.recursos', string='Recurso', required=False, tracking=True)
    evento_id = fields.Many2one(comodel_name='reservaciones.eventos', string='Evento', required=True, tracking=True)
    dias = fields.Char(string='Días', required=False, tracking=True)
