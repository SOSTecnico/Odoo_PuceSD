from odoo import fields, models, api


class Reserva(models.Model):
    _name = 'reservas.reservaciones'
    _description = 'Reservas: Reservación'
    _rec_name = 'codigo'

    codigo = fields.Char(string='Código Reserva')
    laboratorio_id = fields.Many2one(comodel_name='reservas.laboratorios', string='Laboratorio', required=True)
    responsable_id = fields.Many2one(comodel_name='hr.employee', string='Responsable', required=True)
    asignatura_id = fields.Many2one(comodel_name='reservas.asignaturas', string='Asignatura', required=False)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_final = fields.Date(string='Fecha Final', required=True)

    detalle_reserva_id = fields.One2many(comodel_name='reservas.detalle_reservacion', inverse_name='reserva_id',
                                         string='Detalle de Reservación', required=False)


class DetalleReserva(models.Model):
    _name = 'reservas.detalle_reservacion'
    _description = 'Reservas: Detalle Reserva'

    reserva_id = fields.Many2one(comodel_name='reservas.reservaciones', string='Reserva', required=False)
    fecha_inicio = fields.Datetime(string='Fecha y Hora Inicio', required=False)
    fecha_fin = fields.Datetime(string='Fecha y Hora Fin', required=False)
