from datetime import datetime, timedelta
import random
import pytz

from odoo import fields, models, api
from odoo.exceptions import ValidationError


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
    recurso_id = fields.Many2one(comodel_name='reservaciones.recursos', string='Recurso', required=True, tracking=True)
    evento_id = fields.Many2one(comodel_name='reservaciones.eventos', string='Evento', required=True, tracking=True)
    dias = fields.Char(string='Días', required=False, tracking=True)
    ambiente = fields.Selection(string='Ambiente', selection=[('a', 'A'), ('b', 'B'), ], required=False, tracking=True)

    detalle_reserva_id = fields.One2many(comodel_name='reservaciones.detalle_reserva', inverse_name='reserva_id',
                                         string='Detalle de Reserva', required=False)

    @api.onchange('fecha_inicio')
    def onchange_fecha_inicio(self):
        if self.fecha_inicio:
            if not self.fecha_fin:
                self.fecha_fin = self.fecha_inicio

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fecha_inicio_fecha_fin(self):
        for record in self:
            if record.fecha_inicio > record.fecha_fin:
                raise ValidationError("La Fecha de Inicio no puede ser menor que la Fecha Final")

    @api.constrains('hora_inicio', 'hora_fin')
    def _check_hora_inicio_hora_fin(self):
        for record in self:
            if record.hora_inicio >= record.hora_fin:
                raise ValidationError("La Hora de Inicio no puede ser menor o igual que la Hora Final")

    def generar_detalle_reserva(self):

        # DATOS DE INFORMACIÓN
        fecha_inicio = self.fecha_inicio
        fecha_fin = self.fecha_fin
        tz = pytz.timezone('UTC')
        hora_inicio = (datetime.min + timedelta(hours=self.hora_inicio)).time()
        hora_fin = (datetime.min + timedelta(hours=self.hora_fin)).time()

        # MODELO DETALLE RESERVA
        detalle_reserva = self.env['reservaciones.detalle_reserva']

        # Si la reserva no es concurrente, se genera un solo registro
        if fecha_inicio == fecha_fin:
            inicio = datetime.combine(fecha_inicio, hora_inicio)
            fin = datetime.combine(fecha_inicio, hora_fin)

            detalle_reserva.create({
                'inicio': inicio + timedelta(hours=5),
                'fin': fin + timedelta(hours=5),
                'reserva_id': self.id
            })

    @api.model
    def create(self, values):
        # Add code here
        res = super(Reserva, self).create(values)
        res.codigo = f"{datetime.now().strftime('%Y%d')}-{random.randint(1000, 9999)}"
        res.generar_detalle_reserva()
        return res


class DetalleReserva(models.Model):
    _name = 'reservaciones.detalle_reserva'
    _description = 'Detalle Reserva'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(related='reserva_id.evento_id.name')
    inicio = fields.Datetime(string='Inicio', required=False, tracking=True)
    fin = fields.Datetime(string='Fin', required=False, tracking=True)
    reserva_id = fields.Many2one(comodel_name='reservaciones.reservas', string='Reserva', required=False,
                                 ondelete='cascade', tracking=True)
