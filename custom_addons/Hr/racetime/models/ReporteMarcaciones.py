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
        # Día:25 - Ya basta freezeeer, ya manden a las casas...

        # Empezamos con la fecha inicio
        fecha_ = self.fecha_inicio

        # Obtenemos los horarios
        horarios = self.env['racetime.asignacion_horario'].sudo().search([('fecha_fin', '=', False)])
        if not horarios:
            raise ValidationError('Para realizar los cálculos por favor debe existir al menos un horario disponible')

        for empleado in self.empleados_ids:
            print("-------------EMPLEADO---------------")
            print(empleado.name)
            # Horarios disponibles de cada empleado
            horarios_empleado = horarios.filtered_domain([('empleado_id', '=', empleado.id)])

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
                [('empleado_id', '=', empleado.id), ('desde_fecha', '>=', self.fecha_inicio)])
            horario_activo = None
            while fecha_ <= self.fecha_fin:
                es_feriado = False

                # Calculo de Feriados
                for fer in feriados:
                    if fecha_ >= fer.desde and fecha_ <= fer.hasta:
                        es_feriado = True
                if not es_feriado:
                    # Calculo para los permisos
                    permiso = permisos_del_empleado.filtered_domain(
                        [('desde_fecha', '<=', fecha_), ('hasta_fecha', '>=', fecha_)])

                    # primer caso dia completo
                    if permiso.estado == 'aprobado':
                        if permiso.todo_el_dia:
                            marcaciones = self.generar_registros_en_blanco(fecha=fecha_, empleado=empleado,
                                                                           observacion='permiso', permiso=permiso)
                            self.registrar_marcaciones(marcaciones=marcaciones)
                            fecha_ = fecha_ + timedelta(days=1)
                            continue

                    for h in horarios_empleado:
                        if fecha_.strftime("%A") in h.dias.mapped('name'):
                            horario_activo = h
                            marcaciones_del_dia = marcaciones_empleado.filtered(
                                lambda f: f.fecha_hora.date() == fecha_)
                            registros = self.calcular_marcaciones(marcaciones=marcaciones_del_dia,
                                                                  horario=horario_activo, permisos=permiso)
                            marcaciones = self.calcular_tiempos(registros=registros, empleado=empleado,
                                                                fecha=fecha_,
                                                                permisos=permisos_del_empleado)
                            print(marcaciones)
                            # permisos por intervalo de hora

                            self.registrar_marcaciones(marcaciones=marcaciones)
                            break
                        else:
                            marcaciones = self.generar_registros_en_blanco(fecha=fecha_, empleado=empleado,
                                                                           observacion='no_aplica')
                            self.registrar_marcaciones(marcaciones=marcaciones)
                            break
                else:
                    # Aqui toca hacer un metodo para los feriados
                    marcaciones = self.generar_registros_en_blanco(fecha=fecha_, empleado=empleado,
                                                                   observacion='feriado')
                    self.registrar_marcaciones(marcaciones=marcaciones)
                fecha_ = fecha_ + timedelta(days=1)
            fecha_ = self.fecha_inicio

        #    raise ValidationError('posi')

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
    # este sistema siempre será NEMESIS
    def calcular_marcaciones(self, marcaciones, horario, permisos):
        if permisos:
            N1 = timedelta(hours=(horario.marcacion_1 + 5))
            N2 = timedelta(hours=(horario.marcacion_2 + 5))
            N3 = timedelta(hours=(horario.marcacion_3 + 5))
            N4 = timedelta(hours=(horario.marcacion_4 + 5))
            P1 = timedelta(hours=(permisos.desde_hora + 5))
            P2 = timedelta(hours=(permisos.hasta_hora + 5))

            horarioypermiso = []

            HORARIO = [N1, N2, N3, N4, P1, P2]
            HORARIO = sorted(HORARIO)

            for i in range(len(HORARIO) - 1):
                pint = (HORARIO[i + 1] - HORARIO[i]) / 2
                nint1 = HORARIO[i] + pint
                nint2 = nint1 + pint
                horarioypermiso.append(nint1)
                horarioypermiso.append(nint2)

            horarioypermiso.insert(0, N1)
            marcacion1 = {"F", False}
            marcacion2 = {"F", False}
            marcacion3 = {"F", False}
            marcacion4 = {"F", False}
            marcacion5 = {"F", False}
            marcacion6 = {"F", False}

            for m in marcaciones:
                value = timedelta(hours=m.fecha_hora.time().hour, minutes=m.fecha_hora.time().minute,
                                  seconds=m.fecha_hora.time().second)
                if value <= horarioypermiso[0]:
                    marcacion1 = m
                elif value > horarioypermiso[0] and value <= horarioypermiso[1]:
                    marcacion1 = m
                elif value > horarioypermiso[1] and value <= horarioypermiso[2]:
                    marcacion2 = m
                elif value > horarioypermiso[2] and value <= horarioypermiso[3]:
                    marcacion2 = m
                elif value > horarioypermiso[3] and value <= horarioypermiso[4]:
                    marcacion3 = m
                elif value > horarioypermiso[4] and value <= horarioypermiso[5]:
                    marcacion3 = m
                elif value > horarioypermiso[5] and value <= horarioypermiso[6]:
                    marcacion4 = m
                elif value > horarioypermiso[6] and value <= horarioypermiso[7]:
                    marcacion4 = m
                elif value > horarioypermiso[7] and value <= horarioypermiso[8]:
                    marcacion5 = m
                elif value > horarioypermiso[8] and value <= horarioypermiso[9]:
                    marcacion5 = m
                elif value > horarioypermiso[9] and value <= horarioypermiso[10]:
                    marcacion6 = m
                elif value > horarioypermiso[10]:
                    marcacion6 = m

            marprevper = [marcacion1, marcacion2, marcacion3, marcacion4, marcacion5, marcacion6]

            # OPTIMIZACION AGREGAR PERMISOS PORQUE ENTRE PERMISOS NO PODRÍA HABER MARCACIONES
            rangoperini = 0
            rangoperfin = 0
            for i in range(len(horarioypermiso)):
                if horarioypermiso[i] == P1:
                    rangoperini = i
                if horarioypermiso[i] == P2:
                    rangoperfin = i

            diccionarioper = {}
            diccionarioper["0"] = 0  # m1
            diccionarioper["2"] = 1  # m2
            diccionarioper["4"] = 2  # m3
            diccionarioper["6"] = 3  # m4
            diccionarioper["8"] = 4  # m5
            diccionarioper["10"] = 5  # m6
            cont = 0
            vueltas = diccionarioper[str(rangoperfin)] - diccionarioper[str(rangoperini)]

            for y in range(vueltas + 1):
                if y is not False:
                    marprevper[diccionarioper[str(rangoperini)] + cont] = {
                        "P": marprevper[diccionarioper[str(rangoperini)] + cont]}
                    cont = cont + 1
                else:
                    marprevper[diccionarioper[str(rangoperini)] + cont] = {"P", False}

            ############################################################################################
            perm = {}
            marc = {}
            contadorp = 0
            contadorm = 0
            for o in marprevper:
                if "P" in o:
                    if "F" in o["P"]:
                        perm[contadorp] = False
                        contadorp = contadorp + 1
                    else:
                        perm[contadorp] = o["P"]
                        contadorp = contadorp + 1
                else:
                    if "F" in o:
                        marc[contadorm] = False
                        contadorm = contadorm + 1
                    else:
                        marc[contadorm] = o
                        contadorm = contadorm + 1

            return {
                'marcaciones': marc,
                'horas': [N1, N2, N3, N4],
                'permisos': perm,
                'horasP': [P1, P2],
                'id_permiso': permisos

            }
        else:
            N1 = timedelta(hours=(horario.marcacion_1 + 5))
            N2 = timedelta(hours=(horario.marcacion_2 + 5))
            N3 = timedelta(hours=(horario.marcacion_3 + 5))
            N4 = timedelta(hours=(horario.marcacion_4 + 5))

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
                if diferencia_1 > tolerancia:
                    observacion_1 = 'atraso'
                    diferencia_1 = diferencia_1 - tolerancia
                else:
                    observacion_1 = 'a_tiempo'

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
                if diferencia_3 > tolerancia:
                    observacion_3 = 'atraso'
                    diferencia_3 = diferencia_3 - tolerancia
                else:
                    observacion_3 = "a_tiempo"
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

        if "permisos" in registros:

            # -----------------permiso-----------------------
            if registros['permisos'][0]:
                marcacion = timedelta(hours=registros['marcaciones'][3].fecha_hora.time().hour,
                                      minutes=registros['marcaciones'][3].fecha_hora.time().minute,
                                      seconds=registros['marcaciones'][3].fecha_hora.time().second)

                if marcacion > registros['horasP'][0]:
                    diferencia_5 = marcacion - registros['horasP'][0]
                    observacion_5 = 'a_tiempo'
                else:
                    diferencia_5 = registros['horasP'][0] - marcacion
                    observacion_5 = 'a_tiempo'
            else:
                diferencia_5 = timedelta(seconds=0)
                observacion_5 = 'a_tiempo'

            # -------------------permiso------------------------
            if registros['permisos'][1]:
                marcacion = timedelta(hours=registros['marcaciones'][3].fecha_hora.time().hour,
                                      minutes=registros['marcaciones'][3].fecha_hora.time().minute,
                                      seconds=registros['marcaciones'][3].fecha_hora.time().second)

                if marcacion > registros['horasP'][1]:
                    diferencia_6 = marcacion - registros['horasP'][1]
                    observacion_6 = 'a_tiempo'
                else:
                    diferencia_6 = registros['horasP'][1] - marcacion
                    observacion_6 = 'a_tiempo'
            else:
                diferencia_6 = timedelta(seconds=0)
                observacion_6 = 'a_tiempo'

            observaciones = [observacion_1, observacion_2, observacion_3, observacion_4]
            observaciones_per = [observacion_5, observacion_6]
            diferencia = [diferencia_1, diferencia_2, diferencia_3, diferencia_4]
            diferencia_per = [diferencia_5, diferencia_6]
            respuesta_marc = []
            respuesta_perm = []

            for i in range(len(registros['marcaciones'])):
                respuesta_marc.insert(i, {
                    'marcacion_id': registros['marcaciones'][i].id if registros['marcaciones'][i] else False,
                    'horario': datetime.combine(fecha, (datetime.min + registros['horas'][i]).time()),
                    'observacion': observaciones[i],
                    'empleado_id': empleado.id,
                    'diferencia': diferencia[i].total_seconds() / 60,
                    'fecha': fecha
                })
            for j in range(len(registros['permisos'])):
                respuesta_perm.insert(j, {
                    'marcacion_id': registros['permisos'][j].id if registros['permisos'][j] else False,
                    'horario': datetime.combine(fecha, (datetime.min + registros['horasP'][j]).time()),
                    'observacion': observaciones_per[j],
                    'empleado_id': empleado.id,
                    'diferencia': diferencia_per[j].total_seconds() / 60,
                    'fecha': fecha,
                    'permiso_id': registros["id_permiso"].id
                })
            respuesta = respuesta_marc + respuesta_perm
            print(respuesta_perm)
            return [respuesta]

        else:
            observaciones = [observacion_1, observacion_2, observacion_3, observacion_4]
            diferencia = [diferencia_1, diferencia_2, diferencia_3, diferencia_4]
            respuesta = []

            for i in range(len(registros['marcaciones'])):
                respuesta.insert(i, {
                    'marcacion_id': registros['marcaciones'][i].id if registros['marcaciones'][i] else False,
                    'horario': datetime.combine(fecha, (datetime.min + registros['horas'][i]).time()),
                    'observacion': observaciones[i],
                    'empleado_id': empleado.id,
                    'diferencia': diferencia[i].total_seconds() / 60,
                    'fecha': fecha
                })

            return [
                respuesta
            ]

    def registrar_marcaciones(self, marcaciones):
        for m in marcaciones:
            self.env['racetime.reporte_marcaciones'].create(m)

    def generar_registros_en_blanco(self, fecha, empleado, observacion, permiso=None):

        datos = {
            'marcacion_id': False,
            'horario': datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=5, minute=0, second=0),
            'observacion': observacion,
            'fecha': fecha,
            'empleado_id': empleado.id,
            'diferencia': timedelta(seconds=0).total_seconds() / 60,
            'permiso_id': permiso.id if permiso else None
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
                                              ('feriado', 'FERIADO'), ('no_aplica', 'NO APLICA'),
                                              ('permiso', 'PERMISO')], )

    marcacion_tiempo = fields.Datetime(string='Marcación Empleado', required=False, related='marcacion_id.fecha_hora',
                                       store=True)

    horario = fields.Datetime(string='Horario', required=False)

    fecha = fields.Date(string='Fecha', required=False)

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=False)

    permiso_id = fields.Many2one(comodel_name='racetime.permisos', string='Permiso', required=False)



    hora = fields.Char(string='Hora', required=False, compute='_hora')
    marcacion = fields.Char(string='Hora Marcación', required=False, compute='_hora')

    @api.depends('horario','marcacion')
    def _hora(self):
        for rec in self:
            rec.hora = (rec.horario - timedelta(hours=5)).strftime("%H:%M")
            rec.marcacion =  (rec.marcacion_tiempo - timedelta(hours=5)).strftime("%H:%M") if rec.marcacion_tiempo else None


