from fileinput import filename

import xlsxwriter
from datetime import datetime, timedelta
from odoo import fields, models, api
import calendar
from openpyxl.utils import get_column_letter

from odoo.exceptions import ValidationError


class ReporteAtrasosWizard(models.TransientModel):
    _name = 'racetime.reporte_atrasos'
    _description = 'Reporte Atrasos'

    name = fields.Char()

    empleados_id = fields.Many2many(comodel_name='hr.employee', string='Empleados', required=True)
    fecha_inicio = fields.Datetime(string='Fecha Inicial', required=True)
    fecha_final = fields.Datetime(string='Fecha Final', required=False)

    def generar_reporte(self):
        data = {
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_final,
            'empleados_ids': self.empleados_id.mapped('id')
        }
        return self.env.ref("racetime.reporte_atrasos_report_xlsx").report_action(self, data=data)

    def generar_reporte_novedades_marcaciones(self):
        data = {
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_final,
            'empleados_ids': self.empleados_id.mapped('id')
        }
        return self.env.ref("racetime.reporte_novedades_marcaciones_report_xlsx").report_action(self, data=data)


class ReporteAtrasosReport(models.AbstractModel):
    _name = 'report.racetime.reporte_atrasos'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Reporte Atrasos'

    def generate_xlsx_report(self, workbook, data, records):
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        sheet = workbook.add_worksheet("Reporte de Atrasos Desempeño")
        bold = workbook.add_format({'bold': True})
        sheet.merge_range("A1:B1", f"Desde: {fecha_inicio} || Hasta: {fecha_fin}", bold)

        sheet.write("B2", "Fecha", bold)
        sheet.write("C2", "Horario", bold)
        sheet.write("D1", "REPORTE DE ATRASOS", bold)
        sheet.write("D2", "Marcación Empleado", bold)
        sheet.write("E2", "Diferencia en minutos", bold)
        sheet.write("F2", "Observaciones", bold)
        sheet.write("G2", "Permisos", bold)

        sheet.set_column('A:A', 45)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 50)

        # ***********************
        empleado = self.env["hr.employee"].search([('id', 'in', data['empleados_ids'])])

        marcaciones = self.env["racetime.reporte_marcaciones"].search(
            [('empleado_id', 'in', data['empleados_ids']), ('observacion', '=', 'atraso'),
             ('marcacion_tiempo', '>=', data['fecha_inicio']), ('marcacion_tiempo', '<=', data['fecha_fin'])],
            order='empleado_id ASC,marcacion_tiempo ASC')

        empleados = marcaciones.mapped('empleado_id')
        celda_inicio = 3
        for i, empleado in enumerate(empleados):
            sheet.write(f"A{celda_inicio}", empleado.name)
            sheet.write(f"D{celda_inicio}", "Numero de atrasos")

            marc = marcaciones.filtered_domain([('empleado_id', '=', empleado.id), ('detalle', '=', 'ed')])
            sheet.write(f"E{celda_inicio}", len(marc))
            celda_inicio = celda_inicio + 1
            insert = timedelta(hours=0, minutes=0, seconds=0)
            total_minutos = timedelta(minutes=0)

            for j, m in enumerate(marc):
                hora, minuto, segundo = m.diferencia_en_minutos.split(":")
                total_minutos = total_minutos + timedelta(minutes=float(minuto) - 5)
                insert = insert + timedelta(hours=float(hora), minutes=float(minuto), seconds=float(segundo))

                horat = m.marcacion_tiempo + timedelta(hours=-5)
                minutos1 = m.marcacion_tiempo + timedelta(minutes=-5)
                atraso1 = m.diferencia_en_minutos.split(":")
                atrasotota = int(atraso1[0])
                if atrasotota < 10:
                    atrasotota = str(atrasotota).zfill(2)
                atrasotota1 = int(atraso1[1]) - 5
                if atrasotota1 < 10:
                    atrasotota1 = str(atrasotota1).zfill(2)
                    print(atrasotota1)

                atrass1 = f'{atrasotota}:{atrasotota1}'

                sheet.write(f"B{celda_inicio + j}", m.marcacion_tiempo.strftime("%Y-%m-%d"))
                sheet.write(f"C{celda_inicio + j}", m.hora)
                sheet.write(f"D{celda_inicio + j}", horat.strftime("%H:%M"))
                # sheet.write(f"E{celda_inicio + j}", minutos1.strftime("00:%M"))
                sheet.write(f"E{celda_inicio + j}", atrass1)
                sheet.write(f"F{celda_inicio + j}", m.observacion)
                sheet.write(f"G{celda_inicio + j}", m.permiso_id.name or "")

            sheet.write(f"D{len(marc) + celda_inicio}", " Total minutos ")
            sheet.write(f"E{len(marc) + celda_inicio}", total_minutos.total_seconds() / 60)

            celda_inicio = celda_inicio + len(marc) + 1

            # *****************

        sheet1 = workbook.add_worksheet("Reporte de Atraso Rol")
        sheet1.merge_range("A1:B1", f"Desde: {fecha_inicio} || Hasta: {fecha_fin}", bold)
        bold = workbook.add_format({'bold': True})

        sheet1.write("B2", "Fecha", bold)

        sheet1.write("C2", "Horario", bold)
        sheet1.write("D1", "REPORTE DE ATRASOS", bold)
        sheet1.write("D2", "Marcación Empleado", bold)
        sheet1.write("E2", "Diferencia en minutos", bold)
        sheet1.write("F2", "Observaciones", bold)
        sheet1.write("G2", "Permisos", bold)

        sheet1.set_column('A:A', 45)
        sheet1.set_column('B:B', 15)
        sheet1.set_column('C:C', 20)
        sheet1.set_column('D:D', 20)
        sheet1.set_column('E:E', 20)
        sheet1.set_column('F:F', 15)
        sheet1.set_column('G:G', 50)
        # *************************
        marcaciones2 = self.env["racetime.reporte_marcaciones"].search(
            [('empleado_id', 'in', data['empleados_ids']), ('observacion', '=', 'atraso'),
             ('marcacion_tiempo', '>=', data['fecha_inicio']), ('marcacion_tiempo', '<=', data['fecha_fin'])],
            order='empleado_id ASC,marcacion_tiempo ASC')

        empleados1 = marcaciones2.mapped('empleado_id')
        celda_inicio1 = 3
        for i, empleado in enumerate(empleados1):
            sheet1.write(f"A{celda_inicio1}", empleado.name)
            sheet1.write(f"D{celda_inicio1}", "Numero de atrasos")

            marc = marcaciones2.filtered_domain([('empleado_id', '=', empleado.id), ('detalle', '=', 'dr')])
            sheet1.write(f"E{celda_inicio1}", len(marc))
            celda_inicio1 = celda_inicio1 + 1
            insert1 = timedelta(hours=0, minutes=0, seconds=0)
            total_minutos2 = timedelta(hours=0, minutes=0)

            for j, m in enumerate(marc):
                hora, minuto, segundo = m.diferencia_en_minutos.split(":")

                # Formula para resta de horas con valores absolutos tomando en solo minutos
                res = abs(m.horario.replace(second=0) - m.marcacion_tiempo.replace(second=0))

                total_minutos2 = total_minutos2 + res - timedelta(minutes=5)
                insert1 = insert1 + timedelta(hours=float(hora), minutes=float(minuto), seconds=float(segundo))

                horat1 = m.marcacion_tiempo + timedelta(hours=-5)
                minutot = m.marcacion_tiempo + timedelta(hours=-5, minutes=-5, seconds=-59)

                atraso = m.diferencia_en_minutos.split(":")
                atrasototal = int(atraso[0])
                if atrasototal < 10:
                    atrasototal = str(atrasototal).zfill(2)
                    print(atrasototal)
                atrasototal1 = int(atraso[1]) + 1
                if atrasototal1 < 10:
                    atrasototal1 = str(atrasototal1).zfill(2)

                atrass = f'{atrasototal}:{atrasototal1}'

                sheet1.write(f"B{celda_inicio1 + j}", m.marcacion_tiempo.strftime("%Y-%m-%d"))
                sheet1.write(f"C{celda_inicio1 + j}", m.hora)
                sheet1.write(f"D{celda_inicio1 + j}", horat1.strftime("%H:%M"))
                # sheet1.write(f"E{celda_inicio1 + j}", minutot.strftime("%H:%M"))
                sheet1.write(f"E{celda_inicio1 + j}", atrass)
                sheet1.write(f"F{celda_inicio1 + j}", m.observacion)
                sheet1.write(f"G{celda_inicio1 + j}", m.permiso_id.name or "")

            sheet1.write(f"D{len(marc) + celda_inicio1}", " Total minutos ")
            sheet1.write(f"E{len(marc) + celda_inicio1}", total_minutos2.total_seconds() / 60)

            celda_inicio1 = celda_inicio1 + len(marc) + 1
            # print(atrass)
            # print(minutot)
            # print(m.diferencia_en_minutos)


class ReporteAtrasosReport(models.AbstractModel):
    _name = 'report.racetime.reporte_novedades_marcaciones'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Reporte Novedades Marcaciones'

    def generate_xlsx_report(self, workbook, data, records):
        fecha_inicio =  datetime.strptime(data['fecha_inicio'], "%Y-%m-%d %H:%M:%S")
        fecha_fin =  datetime.strptime(data['fecha_fin'], "%Y-%m-%d %H:%M:%S")
        sheet = workbook.add_worksheet("Reporte de Atrasos Desempeño")
        bold = workbook.add_format({'bold': True})
        sheet.merge_range("A1:B1", f"Desde: {fecha_inicio} || Hasta: {fecha_fin}", bold)
        nombre_mes_inicio = datetime.strptime(data['fecha_inicio'], "%Y-%m-%d %H:%M:%S").strftime("%B")

        f_temp = fecha_inicio

        #while f_temp < fecha_fin:
        #    print(f_temp.strftime("%d"))
        #    f_temp = f_temp + timedelta(days=1)

       # raise ValidationError("Error")

        # IMPRESION DE LOS DÍAS
        #mes_actual = datetime.now().month
        #calendario_actual = calendar.monthcalendar(datetime.now().year, mes_actual)

        sheet.write("A3", "NOMBRES", bold)
        sheet.write("B2", nombre_mes_inicio, bold)

        sheet.set_column('A:A', 45)
        sheet.set_column('B:AD', 10)

        # impresión de los días
        columna_dias = 1  # Comienza en la columna B

        #POR FOR
        #for asd in range(fecha_inicio, fecha_fin):
        #    sheet.write(f"{get_column_letter(columna_dias)}3", asd)
        #    columna_dias += 1


        #CONSERVANDO EL WHILE
        while f_temp < fecha_fin:
            sheet.write(2, columna_dias, f_temp.strftime('%d'))
            columna_dias += 1
            f_temp += timedelta(days=1)


        empleado = self.env["hr.employee"].search([('id', 'in', data['empleados_ids'])])

        marcaciones = self.env["racetime.reporte_marcaciones"].search(
            [('empleado_id', 'in', data['empleados_ids']), ('marcacion_tiempo', '>=', data['fecha_inicio']),
             ('marcacion_tiempo', '<=', data['fecha_fin'])],
            order='empleado_id ASC,marcacion_tiempo ASC')

        empleados = marcaciones.mapped('empleado_id')
        celda_inicio = 4
        for i, empleado in enumerate(empleados):
            sheet.write(f"A{celda_inicio}", empleado.name)

            marc = marcaciones.filtered_domain([('empleado_id', '=', empleado.id), ('detalle', '=', 'ed')])

            # Revisar si hay atrasos
            estado_asistencia = "NOVEDAD" if any(m.diferencia_en_minutos for m in marc) else "OK"
            sheet.write(f"E{celda_inicio}", estado_asistencia)  # Mostrar "ATRASO" o "OK"

            celda_inicio = celda_inicio + 1
            insert = timedelta(hours=0, minutes=0, seconds=0)
            total_minutos = timedelta(minutes=0)

            for j, m in enumerate(marc):
                hora, minuto, segundo = m.diferencia_en_minutos.split(":")
                total_minutos = total_minutos + timedelta(minutes=float(minuto) - 5)
                insert = insert + timedelta(hours=float(hora), minutes=float(minuto), seconds=float(segundo))

                horat = m.marcacion_tiempo + timedelta(hours=-5)
                minutos1 = m.marcacion_tiempo + timedelta(minutes=-5)
                atraso1 = m.diferencia_en_minutos.split(":")
                atrasotota = int(atraso1[0])
                if atrasotota < 10:
                    atrasotota = str(atrasotota).zfill(2)
                atrasotota1 = int(atraso1[1]) - 5
                if atrasotota1 < 10:
                    atrasotota1 = str(atrasotota1).zfill(2)

                atrass1 = f'{atrasotota}:{atrasotota1}'

            celda_inicio = celda_inicio + len(marc) + 1

