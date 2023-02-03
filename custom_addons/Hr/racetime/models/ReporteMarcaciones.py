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
        # Día:1 - Aquí yaceran todas las ilusiones de tener un sistema perfecto para calcular las horas y marcaciones
        # de ingreso de los empleados, se presentarán inconvenientes y ocurrirán errores pero ahí vamos, con fé
        # que de todas formas toca hacerlo... se irá actualizando este mensaje conforme avanza el proyecto.

        # Empezamos con la fecha inicio
        fecha_ = self.fecha_inicio

        # Obtenemos los horarios
        horarios = self.env['racetime.horarios'].sudo().search([])
        if not horarios:
            raise ValidationError('Para realizar los cálculos por favor debe existir al menos un horario disponible')

        reglas = self.env['racetime.reglas'].search([])

        for empleado in self.empleados_ids:
            print("-------------EMPLEADO---------------", empleado.name)
            # Horarios disponibles de cada empleado
            horarios_empleado = horarios.filtered_domain([('empleados_ids', 'in', empleado.id)])

            marcaciones_empleado = self.env['racetime.detalle_marcacion'].sudo().search(
                [('emp_code', '=', empleado.emp_code), ('fecha_hora', '>=', self.fecha_inicio),
                 ('fecha_hora', '<=', self.fecha_fin)], order="fecha_hora asc")

            marcaciones_calculadas = self.env['racetime.reporte_marcaciones'].search(
                [('empleado_id', '=', empleado.id), ('marcacion_tiempo', '>=', self.fecha_inicio),
                 ('marcacion_tiempo', '<=', self.fecha_fin)])

            marcaciones_calculadas.unlink()

            if 'flexible' in horarios_empleado.mapped('tipo'):
                pass
            else:
                while fecha_ <= self.fecha_fin:
                    # Variable para guardar el horario activo y hacer comparaciones con las marcaciones
                    h_activo = None
                    for horario in horarios_empleado:
                        if fecha_ >= horario.fecha_inicio and fecha_ <= horario.fecha_fin:
                            h_activo = horario

                    marcaciones_del_dia = marcaciones_empleado.filtered(lambda f: f.fecha_hora.date() == fecha_)
                    self.calcular_marcaciones(marcaciones=marcaciones_del_dia, horario=h_activo, reglas=reglas)
                    raise ValidationError('posi')
                    # registros = self.generar_datos_marcacion(marcaciones_del_dia, h_activo, reglas, fecha_)

                    # if registros:
                    #     self.crear_registros_marcacion(registros, empleado)
                    fecha_ = fecha_ + timedelta(days=1)
                fecha_ = self.fecha_inicio
        return {
            'type': 'tree',
            'name': 'Reporte de Marcaciones',
            'view_mode': 'tree,form',
            'res_model': 'racetime.reporte_marcaciones',
            'type': 'ir.actions.act_window',
            'target': 'main'
        }

    # NUEVO METODO
    def calcular_marcaciones(self, marcaciones, horario, reglas):

        marcaciones_fijas = []

        self.calcular_horas(marcaciones=marcaciones[0], horario=horario.hora_inicio, tipo='ingreso', reglas=reglas)
        self.calcular_horas(marcaciones=marcaciones[1], horario=horario.inicio_descanso, tipo='ingreso',
                            reglas=reglas)
        self.calcular_horas(marcaciones=marcaciones[2], horario=horario.fin_descanso, tipo='ingreso', reglas=reglas)
        self.calcular_horas(marcaciones=marcaciones[3], horario=horario.hora_fin, tipo='ingreso', reglas=reglas)

    def generar_marcaciones_para_calcular(self, marcacion, horario, tipo):
        m = timedelta(hours=marcacion.fecha_hora.time().hour, minutes=marcacion.fecha_hora.time().minute,
                      seconds=marcacion.fecha_hora.time().second)
        hora_inicio = timedelta(hours=(horario.hora_inicio + 5))
        hora_fin = timedelta(hours=(horario.hora_fin + 5))
        inicio_descanso = timedelta(hours=(horario.inicio_descanso + 5))
        fin_descanso = timedelta(hours=(horario.fin_descanso + 5))

        if tipo == 'ingreso':
            return m
        




    def calcular_horas(self, marcaciones, horario, tipo, reglas):

        marcacion = timedelta(hours=marcaciones.fecha_hora.time().hour,
                              minutes=marcaciones.fecha_hora.time().minute,
                              seconds=marcaciones.fecha_hora.time().second)
        hora = timedelta(hours=(horario + 5))
        tolerancia = timedelta(hours=reglas.tolerancia)
        tiempo_consideracion = timedelta(hours=reglas.sin_marcacion)
        datos = {
            'observacion': None,
            'minutos': 0
        }
        print("MARCACION: ", marcacion)
        print("HORA: ", hora)
        print("Tipo: ", tipo)
        if marcacion < hora and tipo == 'ingreso':
            diferencia = hora - marcacion
            datos['observacion'] = 'a_tiempo'
            datos['minutos'] = diferencia
        elif marcacion < hora and tipo == 'salida':
            datos['observacion'] = 'adelanto'
            datos['minutos'] = hora - marcacion
        elif marcacion > hora and tipo == 'ingreso':
            diferencia = marcacion - hora
            if diferencia > tiempo_consideracion:
                datos['observacion'] = 'sin_marcacion'
                datos['minutos'] = 0
            else:
                datos['observacion'] = 'a_tiempo' if diferencia <= tolerancia else 'atraso'
                datos['minutos'] = diferencia
        elif marcacion > hora and tipo == 'salida':
            diferencia = marcacion - hora
            if diferencia > tiempo_consideracion:
                datos['minutos'] = 0
                datos['observacion'] = 'sin_marcacion'
            else:
                datos['minutos'] = diferencia
                datos['observacion'] = 'exceso'
        print(datos)
        print("--------------------")
        return datos

    # def calcular_marcacion(self, marcaciones, hora, tipo, reglas):
    #     datos = {
    #         'observacion': False,
    #         'minutos': 0,
    #         'marcacion_id': None,
    #     }
    #     tiempos = []
    #     tipos_ingresos = []
    #     marcaciones_id = []
    #
    #     tolerancia = timedelta(hours=reglas.tolerancia)
    #
    #     for m in marcaciones:
    #         marcacion = timedelta(hours=m.fecha_hora.time().hour, minutes=m.fecha_hora.time().minute,
    #                               seconds=m.fecha_hora.time().second)
    #
    #         if marcacion < hora and tipo == 'ingreso':
    #             tiempos.append(hora - marcacion)
    #             tipos_ingresos.append('adelanto')
    #             marcaciones_id.append(m)
    #
    #         elif marcacion < hora and tipo == 'salida':
    #             tiempos.append(hora - marcacion)
    #             tipos_ingresos.append('adelanto')
    #             marcaciones_id.append(m)
    #         elif marcacion > hora and tipo == 'ingreso':
    #             tiempos.append(marcacion - hora)
    #             tipos_ingresos.append('atraso')
    #             marcaciones_id.append(m)
    #         elif marcacion > hora and tipo == 'salida':
    #             tiempos.append(marcacion - hora)
    #             tipos_ingresos.append('exceso')
    #             marcaciones_id.append(m)
    #
    #     if marcaciones:
    #         datos['minutos'] = min(tiempos)
    #         datos['observacion'] = tipos_ingresos[tiempos.index(datos['minutos'])]
    #         datos['marcacion_id'] = marcaciones_id[tiempos.index(datos['minutos'])]
    #
    #         if datos['observacion'] == 'atraso':
    #             if datos['minutos'] <= tolerancia:
    #                 datos['observacion'] = 'a_tiempo'
    #
    #         return datos
    #
    # def generar_datos_marcacion(self, marcaciones, horario, reglas, fecha):
    #     datos = []
    #     ingreso = self.calcular_marcacion(marcaciones,
    #                                       timedelta(hours=(horario.hora_inicio + 5)), 'ingreso',
    #                                       reglas)
    #     if ingreso:
    #         ingreso['horario'] = datetime.combine(fecha,
    #                                               (datetime.min + timedelta(hours=(horario.hora_inicio + 5))).time())
    #         datos.append(ingreso)
    #     inicio_descanso = self.calcular_marcacion(marcaciones,
    #                                               timedelta(hours=(horario.inicio_descanso + 5)),
    #                                               'salida', reglas)
    #     if inicio_descanso:
    #         inicio_descanso['horario'] = datetime.combine(fecha, (
    #                 datetime.min + timedelta(hours=(horario.inicio_descanso + 5))).time())
    #         datos.append(inicio_descanso)
    #     fin_descanso = self.calcular_marcacion(marcaciones,
    #                                            timedelta(hours=(horario.fin_descanso + 5)),
    #                                            'ingreso', reglas)
    #     if fin_descanso:
    #         fin_descanso['horario'] = datetime.combine(fecha, (
    #                 datetime.min + timedelta(hours=(horario.fin_descanso + 5))).time())
    #         datos.append(fin_descanso)
    #     salida = self.calcular_marcacion(marcaciones,
    #                                      timedelta(hours=(horario.hora_fin + 5)), 'salida',
    #                                      reglas)
    #     if salida:
    #         salida['horario'] = datetime.combine(fecha, (
    #                 datetime.min + timedelta(hours=(horario.hora_fin + 5))).time())
    #         datos.append(salida)
    #
    #     for t in datos:
    #         print(t)
    #
    #     return datos
    #
    # def crear_registros_marcacion(self, datos, empleado):
    #     for m in datos:
    #         self.env['racetime.reporte_marcaciones'].create({
    #             'marcacion_id': m['marcacion_id'].id,
    #             'diferencia': (m['minutos'].total_seconds() / 60),
    #             'observacion': m['observacion'],
    #             'empleado_id': empleado.id,
    #             'horario': m['horario']
    #         })


class ReporteMarcaciones(models.Model):
    _name = 'racetime.reporte_marcaciones'
    _description = 'Reporte Marcaciones'

    name = fields.Char()
    marcacion_id = fields.Many2one(comodel_name='racetime.detalle_marcacion', string='ID Marcación', required=False)
    diferencia = fields.Float(string='Diferencia', required=False)
    observacion = fields.Selection(string='Observación', required=False,
                                   selection=[('atraso', 'ATRASO'), ('adelanto', 'ADELANTO'), ('exceso', 'EXCESO'),
                                              ('a_tiempo', 'A TIEMPO'), ('sin_marcación', 'SIN MARCACIÓN')], )
    marcacion_tiempo = fields.Datetime(
        string='Marcación Empleado',
        required=False, related='marcacion_id.fecha_hora', store=True)

    horario = fields.Datetime(string='Horario', required=False)

    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado',
        required=False)
