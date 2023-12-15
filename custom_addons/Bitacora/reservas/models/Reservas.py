from datetime import timedelta, datetime, time, timezone
import pytz

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class Dias(models.Model):
    _name = 'reservas.dias'
    _description = 'Reservas: Día'

    name = fields.Char(string='Dia', required=True)


class Reserva(models.Model):
    _name = 'reservas.reservaciones'
    _description = 'Reservas: Reservación'
    _rec_name = 'codigo'

    codigo = fields.Char(string='Código Reserva')
    laboratorio_id = fields.Many2one(comodel_name='reservas.laboratorios', string='Laboratorio', required=True)

    responsable_id = fields.Many2one(comodel_name='hr.employee', string='Responsable', required=True,
                                     domain=[("category_ids", "ilike", "DOCENTE")])

    asignatura_id = fields.Many2one(comodel_name='reservas.asignaturas', string='Asignatura', required=False)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_final = fields.Date(string='Fecha Final', required=True)

    @api.onchange('fecha_inicio')
    def onchange_fecha_inicio(self):
        if self.fecha_inicio:
            self.fecha_final = self.fecha_inicio

    @api.constrains('fecha_inicio', 'fecha_final')
    def _check_fechas(self):
        for rec in self:
            if rec.fecha_inicio > rec.fecha_final:
                raise ValidationError("Error: La fecha de inicio no puede ser menor a la fecha final")

    detalle_reserva_id = fields.One2many(comodel_name='reservas.detalle_reservacion', inverse_name='reserva_id',
                                         string='Detalle de Reservación', required=False)


class DetalleReserva(models.Model):
    _name = 'reservas.detalle_reservacion'
    _description = 'Reservas: Detalle Reserva'

    reserva_id = fields.Many2one(comodel_name='reservas.reservaciones', string='Reserva', required=False)
    dias_ = fields.Many2many(comodel_name='reservas.dias', string='Días')

    hora_inicio = fields.Float(string='Hora Inicio', required=True)
    hora_fin = fields.Float(string='Hora Fin', required=True)

    @api.model
    def create(self, values):
        # Add code here
        res = super(DetalleReserva, self).create(values)

        registros = self.env['reservas.registro_reservas'].search(
            [("inicio", ">=", res.reserva_id.fecha_inicio), ("fin", "<=", res.reserva_id.fecha_final)])

        registros.unlink()

        f_inicio = res.reserva_id.fecha_inicio

        while (f_inicio <= res.reserva_id.fecha_final):

            if f_inicio.strftime("%A") in res.dias_.mapped("name"):
                fecha_inicial = (datetime.min + timedelta(hours=res.hora_inicio)).replace(year=f_inicio.year,
                                                                                          month=f_inicio.month,
                                                                                          day=f_inicio.day)

                fecha_final = (datetime.min + timedelta(hours=res.hora_fin)).replace(year=f_inicio.year,
                                                                                     month=f_inicio.month,
                                                                                     day=f_inicio.day)
                hora_inicio = fecha_inicial.astimezone(pytz.utc)
                hora_fin = fecha_final.astimezone(pytz.utc)

                print(fecha_inicial)
                tz = pytz.timezone('UTC')
                r = tz.localize(fecha_inicial)
                dd = r.astimezone(pytz.utc)
                print(dd)
                raise ValidationError("asd")
                self.env['reservas.registro_reservas'].create({
                    'inicio': hora_inicio.strftime("%Y-%m-%d %H:%M:%S"),
                    'fin': hora_fin.strftime("%Y-%m-%d %H:%M:%S"),
                    'reserva_id': res.reserva_id.id
                })

            f_inicio = f_inicio + timedelta(days=1)

        return res


class RegistroReserva(models.Model):
    _name = 'reservas.registro_reservas'
    _description = 'Reservas: Registro Reserva'

    inicio = fields.Datetime(string='Inicio', required=False)
    fin = fields.Datetime(string='Fin', required=False)
    reserva_id = fields.Many2one(comodel_name='reservas.reservaciones', string='Reservación', required=False)
