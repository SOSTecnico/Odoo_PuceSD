from datetime import datetime, timedelta
import calendar

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ReporteMarcacionesWizard(models.TransientModel):
    _name = 'racetime.calculo_marcaciones'
    _description = 'Reporte de Marcación'

    name = fields.Char()
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True)
    empleados_ids = fields.Many2many(comodel_name='hr.employee', string='Empleados')

    @api.onchange('fecha_inicio', 'fecha_fin')
    def onchange_fechas(self):
        if self.fecha_inicio == False:
            self.fecha_inicio = datetime.now().replace(day=1)

        if self.fecha_fin == False:
            self.fecha_fin = datetime.now()

    def calculo_marcaciones(self):
        # Día:18 - No sé cómo pero ya ha evolucionado esto a tal punto de que ya se puede ver algo en los reportes,
        # esperamos que siga así y que se termine pronto, no sé cuanto más podré resistir :c.

        # Empezamos con la fecha inicio
        fecha_ = self.fecha_inicio

        # Obtenemos los horarios
        horarios = self.env['racetime.horarios'].sudo().search([])
        if not horarios:
            raise ValidationError('Para realizar los cálculos por favor debe existir al menos un horario disponible')

        for empleado in self.empleados_ids:
            print("-------------EMPLEADO---------------", empleado.name)
            # Horarios disponibles de cada empleado
            horarios_empleado = horarios.filtered_domain([('empleados_ids', 'in', empleado.id)])

            marcaciones_empleado = self.env['racetime.detalle_marcacion'].sudo().search(
                [('emp_code', '=', empleado.emp_code), ('fecha_hora', '>=', self.fecha_inicio),
                 ('fecha_hora', '<=', self.fecha_fin)], order="fecha_hora asc")

            marcaciones_calculadas = self.env['racetime.reporte_marcaciones'].search(
                [('empleado_id', '=', empleado.id), ('horario', '>=', self.fecha_inicio),
                 ('horario', '<=', self.fecha_fin)])

            marcaciones_calculadas.unlink()

            # FERIADOS
            feriados = self.env['racetime.feriados'].search(
                ['|', ('desde', '>=', self.fecha_inicio), ('desde', '<=', self.fecha_fin),
                 ('hasta', '>=', self.fecha_inicio), ('hasta', '<=', self.fecha_fin)])

            # PERMISOS
            permisos_del_empleado = self.env['racetime.permisos'].search(
                [('empleado_id', '=', empleado.id), ('desde', '>=', self.fecha_inicio)])

            while fecha_ <= self.fecha_fin:
                es_feriado = False
                for fer in feriados:
                    if fecha_ >= fer.desde and fecha_ <= fer.hasta:
                        es_feriado = True
                if not es_feriado:
                    if 'flexible' in horarios_empleado.mapped('tipo'):
                        pass
                    else:
                        # Variable para guardar el horario activo y hacer comparaciones con las marcaciones
                        h_activo = None
                        for horario in horarios_empleado:
                            if fecha_ >= horario.fecha_inicio and fecha_ <= horario.fecha_fin:
                                h_activo = horario

                        if not h_activo.dias:
                            h_activo.dias = []

                        if fecha_.strftime("%A") in h_activo.dias:
                            marcaciones_del_dia = marcaciones_empleado.filtered(lambda f: f.fecha_hora.date() == fecha_)

                            registros = self.calcular_marcaciones(marcaciones=marcaciones_del_dia, horario=h_activo)

                            marcaciones = self.calcular_tiempos(registros=registros, empleado=empleado, fecha=fecha_,
                                                                permisos=permisos_del_empleado)

                            self.registrar_marcaciones(marcaciones=marcaciones)
                else:
                    # Aqui toca hacer un metodo para los feriados
                    marcaciones = self.generar_registros_feriados(fecha=fecha_, empleado=empleado)
                    self.registrar_marcaciones(marcaciones=marcaciones)
                    pass
                fecha_ = fecha_ + timedelta(days=1)
            fecha_ = self.fecha_inicio

        return {
            'type': 'tree',
            'name': 'Reporte de Marcaciones',
            'context': {'search_default_group_empleado': 1, 'search_default_group_horario': 2,
                        'search_default_group_observacion': 3},
            'view_mode': 'tree,form',
            'res_model': 'racetime.reporte_marcaciones',
            'type': 'ir.actions.act_window',
            'target': 'main'
        }

    # ESTE CÁLCULO LO HIZO MIGUEL PERO EN PHP, se intenta pasarlo a python
    def calcular_marcaciones(self, marcaciones, horario):

        N1 = timedelta(hours=(horario.hora_inicio + 5))
        N2 = timedelta(hours=(horario.inicio_descanso + 5))
        N3 = timedelta(hours=(horario.fin_descanso + 5))
        N4 = timedelta(hours=(horario.hora_fin + 5))

        pint = (N2 - N1) / 2
        nint1 = N1 + pint
        nint2 = nint1 + pint

        pint2 = (N3 - N2) / 2
        nint3 = N2 + pint2
        nint4 = nint3 + pint2

        pint3 = (N4 - N3) / 2
        nint5 = N3 + pint3
        nint6 = nint5 + pint3

        marcacion1 = False
        marcacion2 = False
        marcacion3 = False
        marcacion4 = False

        interhorarios = [N1, nint1, nint2, nint3, nint4, nint5, nint6]

        for m in marcaciones:
            value = timedelta(hours=m.fecha_hora.time().hour, minutes=m.fecha_hora.time().minute,
                              seconds=m.fecha_hora.time().second)

            if value <= interhorarios[0]:
                marcacion1 = m
            elif value > interhorarios[0] and value <= interhorarios[1]:
                marcacion1 = m
            elif value > interhorarios[1] and value <= interhorarios[2]:
                marcacion2 = m
            elif value > interhorarios[2] and value <= interhorarios[3]:
                marcacion2 = m
            elif value > interhorarios[3] and value <= interhorarios[4]:
                marcacion3 = m
            elif value > interhorarios[4] and value <= interhorarios[5]:
                marcacion3 = m
            elif value > interhorarios[5] and value <= interhorarios[6]:
                marcacion4 = m
            elif value > interhorarios[6]:
                marcacion4 = m

        return {
            'marcaciones': [marcacion1, marcacion2, marcacion3, marcacion4],
            'horas': [N1, N2, N3, N4],
        }

    def calcular_tiempos(self, registros, empleado, fecha, permisos):
        reglas = self.env['racetime.reglas'].search([])
        tolerancia = timedelta(hours=reglas.tolerancia)

        if registros['marcaciones'][0]:
            marcacion = timedelta(hours=registros['marcaciones'][0].fecha_hora.time().hour,
                                  minutes=registros['marcaciones'][0].fecha_hora.time().minute,
                                  seconds=registros['marcaciones'][0].fecha_hora.time().second)

            if marcacion > registros['horas'][0]:
                diferencia_1 = marcacion - registros['horas'][0]
                observacion_1 = 'atraso' if diferencia_1 > tolerancia else 'a_tiempo'


            else:
                diferencia_1 = registros['horas'][0] - marcacion
                observacion_1 = 'a_tiempo'
        else:
            diferencia_1 = timedelta(seconds=0)
            observacion_1 = 'sin_marcacion'

        if registros['marcaciones'][1]:
            marcacion = timedelta(hours=registros['marcaciones'][1].fecha_hora.time().hour,
                                  minutes=registros['marcaciones'][1].fecha_hora.time().minute,
                                  seconds=registros['marcaciones'][1].fecha_hora.time().second)

            if marcacion > registros['horas'][1]:
                diferencia_2 = marcacion - registros['horas'][1]
                observacion_2 = 'exceso'
            else:
                diferencia_2 = registros['horas'][1] - marcacion
                observacion_2 = 'adelanto'
        else:
            diferencia_2 = timedelta(seconds=0)
            observacion_2 = 'sin_marcacion'

        if registros['marcaciones'][2]:
            marcacion = timedelta(hours=registros['marcaciones'][2].fecha_hora.time().hour,
                                  minutes=registros['marcaciones'][2].fecha_hora.time().minute,
                                  seconds=registros['marcaciones'][2].fecha_hora.time().second)

            if marcacion > registros['horas'][2]:
                diferencia_3 = marcacion - registros['horas'][2]
                observacion_3 = 'atraso' if diferencia_3 > tolerancia else 'a_tiempo'
            else:
                diferencia_3 = registros['horas'][2] - marcacion
                observacion_3 = 'a_tiempo'
        else:
            diferencia_3 = timedelta(seconds=0)
            observacion_3 = 'sin_marcacion'

        if registros['marcaciones'][3]:
            marcacion = timedelta(hours=registros['marcaciones'][3].fecha_hora.time().hour,
                                  minutes=registros['marcaciones'][3].fecha_hora.time().minute,
                                  seconds=registros['marcaciones'][3].fecha_hora.time().second)

            if marcacion > registros['horas'][3]:
                diferencia_4 = marcacion - registros['horas'][3]
                observacion_4 = 'exceso'
            else:
                diferencia_4 = registros['horas'][3] - marcacion
                observacion_4 = 'adelanto'
        else:
            diferencia_4 = timedelta(seconds=0)
            observacion_4 = 'sin_marcacion'

        return [
            {
                'marcacion_id': registros['marcaciones'][0].id if registros['marcaciones'][0] else False,
                'horario': datetime.combine(fecha, (datetime.min + registros['horas'][0]).time()),
                'observacion': observacion_1,
                'empleado_id': empleado.id,
                'diferencia': diferencia_1.total_seconds() / 60,
                'fecha': fecha
            },
            {
                'marcacion_id': registros['marcaciones'][1].id if registros['marcaciones'][1] else False,
                'horario': datetime.combine(fecha, (datetime.min + registros['horas'][1]).time()),
                'observacion': observacion_2,
                'empleado_id': empleado.id,
                'diferencia': diferencia_2.total_seconds() / 60,
                'fecha': fecha
            },
            {
                'marcacion_id': registros['marcaciones'][2].id if registros['marcaciones'][2] else False,
                'horario': datetime.combine(fecha, (datetime.min + registros['horas'][2]).time()),
                'observacion': observacion_3,
                'empleado_id': empleado.id,
                'diferencia': diferencia_3.total_seconds() / 60,
                'fecha': fecha
            },
            {
                'marcacion_id': registros['marcaciones'][3].id if registros['marcaciones'][3] else False,
                'horario': datetime.combine(fecha, (datetime.min + registros['horas'][3]).time()),
                'observacion': observacion_4,
                'empleado_id': empleado.id,
                'diferencia': diferencia_4.total_seconds() / 60,
                'fecha': fecha
            },
        ]

    def registrar_marcaciones(self, marcaciones):
        for m in marcaciones:
            self.env['racetime.reporte_marcaciones'].create(m)

    def generar_registros_feriados(self, fecha, empleado):

        datos = {
            'marcacion_id': False,
            'horario': datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=5, minute=0, second=0),
            'observacion': 'feriado',
            'empleado_id': empleado.id,
            'diferencia': timedelta(seconds=0).total_seconds() / 60
        }
        return [datos]


class ReporteMarcaciones(models.Model):
    _name = 'racetime.reporte_marcaciones'
    _description = 'Reporte Marcaciones'

    name = fields.Char()
    marcacion_id = fields.Many2one(comodel_name='racetime.detalle_marcacion', string='ID Marcación', required=False)
    diferencia = fields.Float(string='Diferencia', required=False)
    observacion = fields.Selection(string='Observación', required=False,
                                   selection=[('atraso', 'ATRASO'), ('adelanto', 'ADELANTO'), ('exceso', 'EXCESO'),
                                              ('a_tiempo', 'A TIEMPO'), ('sin_marcacion', 'SIN MARCACIÓN'),
                                              ('feriado', 'FERIADO')], )

    marcacion_tiempo = fields.Datetime(string='Marcación Empleado', required=False, related='marcacion_id.fecha_hora',
                                       store=True)

    horario = fields.Datetime(string='Horario', required=False)

    fecha = fields.Date(string='Fecha', required=False)

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=False)

    permiso_id = fields.Many2one(comodel_name='racetime.permisos', string='Permiso', required=False)
