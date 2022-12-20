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

    active = fields.Boolean(string='Active', required=False, default=True)

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
        hora_inicio = (datetime.min + timedelta(hours=self.hora_inicio)).time()
        hora_fin = (datetime.min + timedelta(hours=self.hora_fin)).time()

        detalle_reserva = self.env['reservaciones.detalle_reserva']

        # Si la reserva no es concurrente, se genera un solo registro
        if fecha_inicio == fecha_fin:
            inicio = datetime.combine(fecha_inicio, hora_inicio) + timedelta(hours=5)
            fin = datetime.combine(fecha_inicio, hora_fin) + timedelta(hours=5)

            # Se genera la consulta para obtener todos los horarios que coincidan con:
            # El recurso, la fecha y la hora de inicio y fin
            domain = [
                ('recurso_id', '=', self.recurso_id.id),
                '|',
                '|',
                '&', ('inicio', '<=', inicio), ('fin', '>', inicio),
                '&', ('inicio', '<', fin), ('fin', '>=', fin),
                '&', ('inicio', '>', inicio), ('fin', '<', fin)
            ]

            reservaciones = detalle_reserva.search(domain)
            codigos = []
            for r in reservaciones:
                codigos.append(r.reserva_id.codigo)

            if codigos:
                raise ValidationError("Existe un choque de Horario, Código(s): %s" % codigos)

            detalle_reserva.create({
                'inicio': inicio,
                'fin': fin,
                'reserva_id': self.id
            })
        else:
            # Si la reserva es concurrente(Varias fechas), se genera varios registros en detalle reservas,
            # desde la fecha inicial hasta la fecha final en los horarios establecidos y días seleccionados

            if not self.dias:
                raise ValidationError('Si es un reserva concurrente, debe seleccionar al menos un día')

            fecha_temp = fecha_inicio

            while fecha_temp <= fecha_fin:
                if fecha_temp.strftime("%A").lower() in self.dias:
                    inicio = datetime.combine(fecha_temp, hora_inicio) + timedelta(hours=5)
                    fin = datetime.combine(fecha_temp, hora_fin) + timedelta(hours=5)

                    # Se genera la consulta para obtener todos los horarios que coincidan con:
                    # El recurso, la fecha y la hora de inicio y fin por cada día
                    domain = [
                        ('recurso_id', '=', self.recurso_id.id),
                        '|',
                        '|',
                        '&', ('inicio', '<=', inicio), ('fin', '>', inicio),
                        '&', ('inicio', '<', fin), ('fin', '>=', fin),
                        '&', ('inicio', '>', inicio), ('fin', '<', fin)
                    ]
                    reservaciones = detalle_reserva.search(domain)
                    codigos = []
                    for r in reservaciones:
                        codigos.append(r.reserva_id.codigo)

                    if codigos:
                        raise ValidationError("Existe un choque de Horario, Código(s): %s" % codigos)

                    detalle_reserva.create({
                        'inicio': inicio,
                        'fin': fin,
                        'reserva_id': self.id
                    })
                fecha_temp = fecha_temp + timedelta(days=1)

    @api.model
    def create(self, values):
        # Add code here
        res = super(Reserva, self).create(values)
        res.codigo = f"{datetime.now().strftime('%Y%d')}-{random.randint(1000, 9999)}"

        return res

    def write(self, values):

        res = super(Reserva, self).write(values)

        self.detalle_reserva_id.unlink()
        self.generar_detalle_reserva()

        for detalle_reserva in self.detalle_reserva_id:
            detalle_reserva.active = self.active
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
    recurso_id = fields.Many2one(string='Recurso', required=False, related='reserva_id.recurso_id', store=True)
    responsable_id = fields.Many2one(string='Responsable', required=False, related='reserva_id.responsable_id')

    active = fields.Boolean(string='Active', required=False, default=True)
