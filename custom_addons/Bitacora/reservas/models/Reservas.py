from datetime import timedelta, datetime
from random import randint

import pytz

from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class Dias(models.Model):
    _name = 'reservas.dias'
    _description = 'Reservas: Día'

    name = fields.Char(string='Dia', required=True)


class Reserva(models.Model):
    _name = 'reservas.reservaciones'
    _description = 'Reservas: Reservación'
    _rec_name = 'codigo'

    @api.model
    def codigo_reserva(self):
        year = datetime.now().year
        month = datetime.now().month
        cod = randint(1000, 9999)
        codigo = f"{year}{month}-{cod}"

        rec = self.env['reservas.reservaciones'].search([('codigo', '=', codigo)])
        if not rec:
            return codigo
        else:
            return self.codigo_reserva()

    codigo = fields.Char(string='Código Reserva', default=codigo_reserva, copy=False)
    laboratorio_id = fields.Many2one(comodel_name='reservas.laboratorios', string='Laboratorio', required=True)

    responsable_id = fields.Many2one(comodel_name='hr.employee', string='Responsable', required=True,
                                     domain=[("category_ids", "ilike", "DOCENTE")])

    asignatura_id = fields.Many2one(comodel_name='reservas.asignaturas', string='Asignatura', required=True)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_final = fields.Date(string='Fecha Final', required=True)

    recurrente = fields.Boolean(string='Recurrente', required=False, default=False)
    hora_inicio = fields.Float(string='Hora Inicio', )
    hora_fin = fields.Float(string='Hora Fin', )

    @api.onchange('fecha_inicio')
    def onchange_fecha_inicio(self):
        if self.fecha_inicio:
            self.fecha_final = self.fecha_inicio + timedelta(days=1)

    @api.constrains('fecha_inicio', 'fecha_final', 'hora_inicio', 'hora_fin')
    def _check_fechas(self):
        for rec in self:
            if rec.fecha_inicio > rec.fecha_final:
                raise UserError("La fecha de inicio no puede ser menor a la fecha final")

            if not rec.recurrente and rec.hora_inicio >= rec.hora_fin:
                raise UserError("La Hora de inicio no puede ser igual o menor a la hora fin")

    detalle_reserva_id = fields.One2many(comodel_name='reservas.detalle_reservacion', inverse_name='reserva_id',
                                         string='Detalle de Reservación', required=False)
    registros_reserva_ids = fields.One2many(comodel_name='reservas.registro_reservas', inverse_name='reserva_id',
                                            string='Registros_reserva_ids', required=False)

    @api.constrains('recurrente', 'detalle_reserva_id')
    def _check_recurrencia(self):
        for rec in self:
            if rec.recurrente and len(rec.detalle_reserva_id) == 0:
                raise UserError("No se puede registrar una reservación recurrente sin especificar los días ni la hora")

    @api.model
    def create(self, values):
        res = super(Reserva, self).create(values)
        if not res.recurrente:
            res.crear_registro_reserva()
        return res

    def write(self, values):
        print(values)

        res = super(Reserva, self).write(values)
        if not self.recurrente:
            self.registros_reserva_ids.sudo().unlink()
            self.crear_registro_reserva()
        else:
            self.registros_reserva_ids.search(
                [("detalle_reserva_id", "=", False), ("reserva_id", self.id)]).sudo().unlink()

        return res

    def crear_registro_reserva(self):

        h_i = timedelta(hours=self.hora_inicio)
        h_f = timedelta(hours=self.hora_fin)
        hora_inicio = datetime.combine(self.fecha_inicio, (datetime.min + h_i).time()) + timedelta(hours=5)
        hora_fin = datetime.combine(self.fecha_inicio, (datetime.min + h_f).time()) + timedelta(hours=5)

        self.env["reservas.registro_reservas"].sudo().create({
            "inicio": hora_inicio,
            "fin": hora_fin,
            "reserva_id": self.id
        })
        return True


class DetalleReserva(models.Model):
    _name = 'reservas.detalle_reservacion'
    _description = 'Reservas: Detalle Reserva'

    reserva_id = fields.Many2one(comodel_name='reservas.reservaciones', string='Reserva', required=False,
                                 ondelete='cascade')
    dias = fields.Many2many(comodel_name='reservas.dias', string='Días')

    hora_inicio = fields.Float(string='Hora Inicio', required=True)
    hora_fin = fields.Float(string='Hora Fin', required=True)

    registros_reserva_id = fields.One2many(comodel_name='reservas.registro_reservas', inverse_name='detalle_reserva_id',
                                           string='Registros_reserva_id', required=False)

    @api.constrains("dias")
    def check_dias(self):
        for rec in self:
            if len(rec.dias) == 0:
                raise UserError('No se puede crear la reserva sin especificar los días!!')

    def create(self, values):

        detalle_reserva = super(DetalleReserva, self).create(values)

        for res in detalle_reserva:

            f_inicio = res.reserva_id.fecha_inicio
            f_fin = res.reserva_id.fecha_final

            while (f_inicio <= f_fin):

                if f_inicio.strftime("%A") in res.dias.mapped("name"):

                    hora_inicio = datetime.combine(f_inicio,
                                                   (datetime.min + timedelta(
                                                       hours=res.hora_inicio)).time()) + timedelta(
                        hours=5)

                    hora_fin = datetime.combine(f_inicio,
                                                (datetime.min + timedelta(hours=res.hora_fin)).time()) + timedelta(
                        hours=5)

                    if hora_inicio >= hora_fin:
                        raise ValidationError(
                            "La hora inicial no debe ser inferior a la hora final en el detalle: %s" % res.dias.mapped(
                                "name"))

                    res.sudo().write({
                        "registros_reserva_id": [(0, 0, {
                            "inicio": hora_inicio,
                            "fin": hora_fin,
                            "reserva_id": res.reserva_id.id
                        })]
                    })

                f_inicio = f_inicio + timedelta(days=1)

        return detalle_reserva

    def write(self, vals):
        res = super(DetalleReserva, self).write(vals)

        f_inicio = self.reserva_id.fecha_inicio
        f_fin = self.reserva_id.fecha_final

        self.registros_reserva_id.sudo().unlink()

        while (f_inicio <= f_fin):

            if f_inicio.strftime("%A") in self.dias.mapped("name"):

                hora_inicio = datetime.combine(f_inicio,
                                               (datetime.min + timedelta(hours=self.hora_inicio)).time()) + timedelta(
                    hours=5)

                hora_fin = datetime.combine(f_inicio,
                                            (datetime.min + timedelta(hours=self.hora_fin)).time()) + timedelta(hours=5)

                if hora_inicio >= hora_fin:
                    raise ValidationError(
                        "La hora inicial no debe ser inferior a la hora final en el detalle: %s" % self.dias.mapped(
                            "name"))

                self.env["reservas.registro_reservas"].sudo().create({
                    "inicio": hora_inicio,
                    "fin": hora_fin,
                    "reserva_id": self.reserva_id.id,
                    "detalle_reserva_id": self.id
                })

            f_inicio = f_inicio + timedelta(days=1)
        return res


class RegistroReserva(models.Model):
    _name = 'reservas.registro_reservas'
    _description = 'Reservas: Registro Reserva'
    _rec_name = "asignatura"

    inicio = fields.Datetime(string='Inicio', required=False)
    fin = fields.Datetime(string='Fin', required=False)
    reserva_id = fields.Many2one(comodel_name='reservas.reservaciones', string='Reservación', required=False,
                                 ondelete='cascade')
    detalle_reserva_id = fields.Many2one(comodel_name='reservas.detalle_reservacion', string='Detalle_reserva_id',
                                         required=False, ondelete='cascade')
    asignatura = fields.Char(string='Asignatura', related="reserva_id.asignatura_id.asignatura")
    docente = fields.Char(comodel_name='hr.employee', string='Responsable', related="reserva_id.responsable_id.name")
    laboratorio = fields.Many2one(comodel_name='reservas.laboratorios', string='Laboratorio',
                                  related="reserva_id.laboratorio_id", store=True)

    @api.model
    def create(self, values):

        reservacion = self.env['reservas.reservaciones'].sudo().search([("id", "=", values['reserva_id'])])

        sql = f"""
            SELECT * FROM reservas_registro_reservas 
            WHERE reserva_id <> {values["reserva_id"]} and laboratorio = {reservacion.laboratorio_id.id} and ('{values["inicio"]}' , '{values["fin"]}') overlaps (inicio, fin);

        """

        #            JOIN reservas_registro_reservas ON description
        self.env.cr.execute(sql)
        reservas = self.env.cr.dictfetchall()
        if reservas:
            for reserva in reservas:
                f_i = reserva['inicio'].astimezone(pytz.timezone("America/Guayaquil")).strftime("%H:%M")
                f_f = reserva['fin'].astimezone(pytz.timezone("America/Guayaquil")).strftime("%H:%M")
                fecha_reserva = reserva['inicio'].astimezone(pytz.timezone("America/Guayaquil")).strftime("%Y-%m-%d")
                raise ValidationError("Error: Existe una reserva en el período de tiempo seleccionado."
                                      #f"\nCódido de la reserva: {reservacion.reserva_id.description}"
                                      f"\nLaboratorio: {reserva['laboratorio']}"
                                      f"\nHora de inicio: {f_i}"
                                      f"\nHora de finalización: {f_f}"
                                      f"\nFecha ya programada: {fecha_reserva}"
                                      f"\nAsignatura: {reservacion.asignatura_id.asignatura}")
        res = super(RegistroReserva, self).create(values)

        return res


        # if reservas_existente:
       # f"\nCódigo de la nueva reserva: {values['reserva_id']}")
        #     f_i = reservas_existente[0].inicio.astimezone(pytz.timezone("America/Guayaquil")).strftime("%H:%M")
        #     f_f = reservas_existente[0].fin.astimezone(pytz.timezone("America/Guayaquil")).strftime("%H:%M")
        #     raise ValidationError("Error: El laboratorio ya está reservado para ese periodo de tiempo."
        #                           f"\nDETALLES:"
        #                           f"\nCódigo de la Reserva: {reservas_existente[0].reserva_id.codigo}"
        #                           f"\nFecha: {reservas_existente[0].inicio.date()}"
        #                           f"\nHora: {f_i} - {f_f}")
