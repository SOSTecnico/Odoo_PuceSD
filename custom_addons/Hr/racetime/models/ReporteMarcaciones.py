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
        horarios = self.env['racetime.asignacion_horario'].sudo().search(
            [('fecha_inicio', '>=', self.fecha_inicio)])

        for empleado in self.empleados_ids:
            print("-------------EMPLEADO---------------")
            print(empleado.name)

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
            # Horarios disponibles de cada empleado
            horarios_empleado = horarios.filtered_domain([('empleado_id', '=', empleado.id)])

            while fecha_ <= self.fecha_fin:
                es_feriado = False

                horario_activo = horarios_empleado.filtered_domain(
                    [('fecha_inicio', '<=', fecha_), ('fecha_fin', '>=', fecha_)])

                # Calculo de Feriados
                for fer in feriados:
                    if fecha_ >= fer.desde and fecha_ <= fer.hasta:
                        es_feriado = True
                if not es_feriado:
                    # Calculo para los permisos
                    # print(permisos_del_empleado.desde_fecha)
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

                    for h in horario_activo.horario:
                        print("aaaaa",h)
                        if fecha_.strftime("%A") in h.dias.mapped('name'):
                            marcaciones_del_dia = marcaciones_empleado.filtered(
                                lambda f: f.fecha_hora.date() == fecha_)
                            registros = self.calcular_marcaciones(marcaciones=marcaciones_del_dia,
                                                                  horario=h, permisos=permiso)
                            marcaciones = self.calcular_tiempos(registros=registros, empleado=empleado,
                                                                fecha=fecha_,
                                                                permisos=permisos_del_empleado)
                            print(marcaciones)
                            # permisos por intervalo de hora

                            self.registrar_marcaciones(marcaciones=marcaciones)
                            break
                        else:
                            continue
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

        # raise ValidationError('posi')

        return {
            'type': 'tree',
            'name': 'Reporte de Marcaciones',
            'context': {'search_default_group_empleado': 1, 'search_default_group_horario': 2, 'search_default_fds': 3},
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
            marcacion1 = False
            marcacion2 = False
            marcacion3 = False
            marcacion4 = False
            marcacion5 = False
            marcacion6 = False

            permiso1 = False
            permiso2 = False
            permiso3 = False
            permiso4 = False
            permiso5 = False
            permiso6 = False

            for m in marcaciones:
                value = timedelta(hours=m.fecha_hora.time().hour, minutes=m.fecha_hora.time().minute,
                                  seconds=m.fecha_hora.time().second)
                if value <= horarioypermiso[0]:
                    marcacion1 = {"M": m}
                    permiso1 = m
                elif value > horarioypermiso[0] and value <= horarioypermiso[1]:
                    marcacion1 = {"M": m}
                    permiso1 = m
                elif value > horarioypermiso[1] and value <= horarioypermiso[2]:
                    marcacion2 = {"M": m}
                    permiso2 = m
                elif value > horarioypermiso[2] and value <= horarioypermiso[3]:
                    marcacion2 = {"M": m}
                    permiso2 = m
                elif value > horarioypermiso[3] and value <= horarioypermiso[4]:
                    marcacion3 = {"M": m}
                    permiso3 = m
                elif value > horarioypermiso[4] and value <= horarioypermiso[5]:
                    marcacion3 = {"M": m}
                    permiso3 = m
                elif value > horarioypermiso[5] and value <= horarioypermiso[6]:
                    marcacion4 = {"M": m}
                    permiso4 = m
                elif value > horarioypermiso[6] and value <= horarioypermiso[7]:
                    marcacion4 = {"M": m}
                    permiso4 = m
                elif value > horarioypermiso[7] and value <= horarioypermiso[8]:
                    marcacion5 = {"M": m}
                    permiso5 = m
                elif value > horarioypermiso[8] and value <= horarioypermiso[9]:
                    marcacion5 = {"M": m}
                    permiso5 = m
                elif value > horarioypermiso[9] and value <= horarioypermiso[10]:
                    marcacion6 = {"M": m}
                    permiso6 = m
                elif value > horarioypermiso[10]:
                    marcacion6 = {"M": m}
                    permiso6 = m
            busper = [permiso1, permiso2, permiso3, permiso4, permiso5, permiso6]
            marprevper = [marcacion1, marcacion2, marcacion3, marcacion4, marcacion5, marcacion6]

            # se debe buscar un if para remmplazar la m por P antes de mandar el atributo
            #  print (marprevper)

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
                        "P": busper[diccionarioper[str(rangoperini)] + cont]}
                    cont = cont + 1
                else:
                    marprevper[diccionarioper[str(rangoperini)] + cont] = {"P": False}

            print(marprevper)

            # if P1==N1:
            #     marprevper.pop(0)

            ############################################################################################
            perm = {}
            marc = {}
            contadorp = 0
            contadorm = 0
            P3 = timedelta(seconds=0)
            P4 = timedelta(seconds=0)
            # print(marprevper)

            for o in marprevper:
                if o is False:
                    marc[contadorp] = {'M': False}
                    contadorp = contadorp + 1
                else:
                    marc[contadorp] = o
                    contadorp = contadorp + 1

            # print(marc)

            return {
                'marcaciones': marc,
                'horas': HORARIO,
                'permisos': perm,
                'horasB': [N1, N2, N3, N4],
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
        if 'id_permiso' in registros:
            reglas = self.env['racetime.reglas'].search([])
            tolerancia = timedelta(hours=reglas.tolerancia)

            N1 = registros['horas'].index(registros['horasB'][0])
            N2 = registros['horas'].index(registros['horasB'][1])
            N3 = registros['horas'].index(registros['horasB'][2])
            N4 = registros['horas'].index(registros['horasB'][3])
            P1 = registros['horas'].index(registros['horasP'][0])
            P2 = registros['horas'].index(registros['horasP'][1])

            print(N1)
            print(N2)
            print(N3)
            print(N4)
            print(P1)
            print(P2)

            diccionariohora = {}
            diccionariohora[N1] = {"I": N1}  # m1 {"I","M"}
            diccionariohora[N2] = {"S": N2}  # m2 {"S","M"}
            diccionariohora[N3] = {"I": N3}  # m3 {"I","M"}
            diccionariohora[N4] = {"S": N4}  # m4 {"S","M"}
            diccionariohora[P1] = {"I": P1}  # m5 {"I","P"}
            diccionariohora[P2] = {"S": P2}  # m6 {"S","P"}

            # son 5 posiciones p1=0 y p2 =4 entomnces solo nos interesa las psoiciones que sobren el resto son permisos y estan a tiempo
            # solo interesa p1 p2 y lo que sobre

            index = []
            indexp = []

            for y in range(len(registros['horas'])):

                if y >= P1 and y <= P2:
                    indexp.append(y)
                else:
                    index.append(y)
            print(registros['marcaciones'])
            print(index)
            print(indexp)

            observacion_1 = ""
            observacion_2 = ""
            observacion_3 = ""
            observacion_4 = ""
            observacion_5 = ""
            observacion_6 = ""
            observacion_7 = ""
            observacion_8 = ""

            diferencia_1 = timedelta(seconds=0)
            diferencia_2 = timedelta(seconds=0)
            diferencia_3 = timedelta(seconds=0)
            diferencia_4 = timedelta(seconds=0)
            diferencia_5 = timedelta(seconds=0)
            diferencia_6 = timedelta(seconds=0)
            diferencia_7 = timedelta(seconds=0)
            diferencia_8 = timedelta(seconds=0)

            observaciones = {}
            diferencias = {}
            observacionesp = {}
            diferenciasp = {}

            for z in range(len(index)):
                if "I" in diccionariohora[index[z]]:
                    if "M" in registros['marcaciones'][index[z]] and registros['marcaciones'][index[z]][
                        "M"] is not False:

                        marcacion = timedelta(hours=registros['marcaciones'][index[z]]["M"].fecha_hora.time().hour,
                                              minutes=registros['marcaciones'][index[z]]["M"].fecha_hora.time().minute,
                                              seconds=registros['marcaciones'][index[z]]["M"].fecha_hora.time().second)
                        if marcacion > registros['horas'][index[z]]:
                            diferencia_1 = marcacion - registros['horas'][index[z]]
                            if diferencia_1 > tolerancia:
                                observacion_1 = 'atraso'
                                diferencia_1 = diferencia_1 - tolerancia
                            else:
                                observacion_1 = 'a_tiempo'

                        else:
                            diferencia_1 = registros['horas'][index[z]] - marcacion
                            observacion_1 = 'a_tiempo'
                    else:
                        diferencia_1 = timedelta(seconds=0)
                        observacion_1 = 'sin_marcacion'

                    observaciones[index[z]] = observacion_1
                    diferencias[index[z]] = diferencia_1

                if "S" in diccionariohora[index[z]]:
                    if "M" in registros['marcaciones'][index[z]] and registros['marcaciones'][index[z]][
                        "M"] is not False:
                        marcacion = timedelta(hours=registros['marcaciones'][index[z]]["M"].fecha_hora.time().hour,
                                              minutes=registros['marcaciones'][index[z]]["M"].fecha_hora.time().minute,
                                              seconds=registros['marcaciones'][index[z]]["M"].fecha_hora.time().second)

                        if marcacion > registros['horas'][index[z]]:
                            diferencia_1 = marcacion - registros['horas'][index[z]]
                            observacion_1 = 'exceso'


                        else:
                            diferencia_1 = registros['horas'][index[z]] - marcacion
                            observacion_1 = 'adelanto'
                    else:
                        diferencia_1 = timedelta(seconds=0)
                        observacion_1 = 'sin_marcacion'

                    observaciones[index[z]] = observacion_1
                    diferencias[index[z]] = diferencia_1

            for x in range(len(indexp)):
                if x in diccionariohora:
                    if "I" in diccionariohora[indexp[x]]:
                        if "P" in registros['marcaciones'][indexp[x]] and registros['marcaciones'][indexp[x]][
                            "P"] is not False:

                            marcacion = timedelta(hours=registros['marcaciones'][indexp[x]]["P"].fecha_hora.time().hour,
                                                  minutes=registros['marcaciones'][indexp[x]][
                                                      "P"].fecha_hora.time().minute,
                                                  seconds=registros['marcaciones'][indexp[x]][
                                                      "P"].fecha_hora.time().second)

                            if marcacion > registros['horas'][indexp[x]]:
                                diferencia_1 = marcacion - registros['horas'][indexp[x]]
                                if diferencia_1 > tolerancia:
                                    observacion_1 = 'atraso'
                                    diferencia_1 = diferencia_1 - tolerancia
                                else:
                                    observacion_1 = 'a_tiempo'

                            else:
                                diferencia_1 = registros['horas'][index[x]] - marcacion
                                observacion_1 = 'a_tiempo'
                        else:
                            diferencia_1 = timedelta(seconds=0)
                            observacion_1 = 'sin_marcacion'

                        observacionesp[indexp[x]] = observacion_1
                        diferenciasp[indexp[x]] = diferencia_1

                    if "S" in diccionariohora[indexp[x]]:
                        if "P" in registros['marcaciones'][indexp[x]] and registros['marcaciones'][indexp[x]][
                            "P"] is not False:
                            marcacion = timedelta(hours=registros['marcaciones'][indexp[x]]["P"].fecha_hora.time().hour,
                                                  minutes=registros['marcaciones'][indexp[x]][
                                                      "P"].fecha_hora.time().minute,
                                                  seconds=registros['marcaciones'][indexp[x]][
                                                      "P"].fecha_hora.time().second)
                            if marcacion > registros['horas'][indexp[x]]:
                                diferencia_1 = marcacion - registros['horas'][indexp[x]]
                                observacion_1 = 'exceso'

                            else:
                                diferencia_1 = registros['horas'][indexp[x]] - marcacion
                                observacion_1 = 'adelanto'
                        else:
                            diferencia_1 = timedelta(seconds=0)
                            observacion_1 = 'sin_marcacion'

                        observacionesp[indexp[x]] = observacion_1
                        diferenciasp[indexp[x]] = diferencia_1

            respuesta_marc = []
            respuesta_perm = []

            ###################################RESPUESTAS###############################################
            for i in range(len(index)):
                if "M" in registros['marcaciones'][index[i]]:
                    respuesta_marc.insert(index[i], {
                        'marcacion_id': registros['marcaciones'][index[i]]["M"].id if
                        registros['marcaciones'][index[i]]["M"] else False,
                        'horario': datetime.combine(fecha, (datetime.min + registros['horas'][index[i]]).time()),
                        'observacion': observaciones[index[i]],
                        'empleado_id': empleado.id,
                        'diferencia': diferencias[index[i]].total_seconds() / 60,
                        'fecha': fecha
                    })

            for j in range(len(indexp)):

                if "P" in registros['marcaciones'][indexp[j]] and indexp[j] in observacionesp:
                    respuesta_perm.insert(indexp[j], {
                        'marcacion_id': registros['marcaciones'][indexp[j]]["P"].id if
                        registros['marcaciones'][indexp[j]]["P"] else False,
                        'horario': datetime.combine(fecha, (datetime.min + registros['horas'][indexp[j]]).time()),
                        'observacion': observacionesp[indexp[j]],
                        'empleado_id': empleado.id,
                        'diferencia': diferenciasp[indexp[j]].total_seconds() / 60,
                        'fecha': fecha,
                        'permiso_id': registros['id_permiso'].id
                    })
                if "M" in registros['marcaciones'][indexp[j]] and indexp[j] in observacionesp:
                    respuesta_perm.insert(indexp[j], {
                        'marcacion_id': registros['marcaciones'][indexp[j]]["M"].id if
                        registros['marcaciones'][indexp[j]]["M"] else False,
                        'horario': datetime.combine(fecha, (datetime.min + registros['horas'][indexp[j]]).time()),
                        'observacion': observacionesp[indexp[j]],
                        'empleado_id': empleado.id,
                        'diferencia': diferenciasp[indexp[j]].total_seconds() / 60,
                        'fecha': fecha,
                        'permiso_id': registros['id_permiso'].id
                    })
            return [respuesta_marc + respuesta_perm]
        else:
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

            return [respuesta]

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

    @api.depends('horario', 'marcacion')
    def _hora(self):
        for rec in self:
            rec.hora = (rec.horario - timedelta(hours=5)).strftime("%H:%M")
            rec.marcacion = (rec.marcacion_tiempo - timedelta(hours=5)).strftime(
                "%H:%M") if rec.marcacion_tiempo else None
