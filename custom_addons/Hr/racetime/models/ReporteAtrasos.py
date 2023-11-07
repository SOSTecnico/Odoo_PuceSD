from fileinput import filename

import xlsxwriter
from datetime import datetime, timedelta
from odoo import fields, models, api


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


class ReporteAtrasosReport(models.AbstractModel):
    _name = 'report.racetime.reporte_atrasos'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Reporte Atrasos'

    def generate_xlsx_report(self, workbook, data, records):
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        sheet = workbook.add_worksheet("Reporte de Atrasos")
        bold = workbook.add_format({'bold': True})
        sheet.merge_range("A1:B1", f"Desde: {fecha_inicio} || Hasta: {fecha_fin}", bold)


        sheet.write("B2", "Fecha", bold)
        sheet.write("C2", "Horario", bold)
        sheet.write("D1", "REPORTE DE ATRASOS", bold)
        sheet.write("D2", "Marcacion Empleado", bold)
        sheet.write("E2", "Diferencia en minutos", bold)
        sheet.write("F2", "Observaciones", bold)

        sheet.set_column('A:A', 45)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 15)

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
            sheet.write(f"D{celda_inicio}", "Cantidad de atrasos")

            marc = marcaciones.filtered_domain([('empleado_id', '=', empleado.id)])
            sheet.write(f"E{celda_inicio}", len(marc))
            celda_inicio = celda_inicio + 1
            insert = timedelta(hours=0, minutes=0, seconds=0)

            for j, m in enumerate(marc):
                hora, minuto, segundo = m.diferencia_en_minutos.split(":")

                insert = insert + timedelta(hours=float(hora), minutes=float(minuto), seconds=float(segundo))

                sheet.write(f"B{celda_inicio + j}", m.marcacion_tiempo.strftime("%Y-%m-%d"))
                sheet.write(f"C{celda_inicio + j}", m.hora)
                sheet.write(f"D{celda_inicio + j}", m.marcacion)
                sheet.write(f"E{celda_inicio + j}", m.diferencia_en_minutos)
                sheet.write(f"F{celda_inicio + j}", m.observacion)
            sheet.write(f"D{len(marc) + celda_inicio}", " Total minutos ")
            sheet.write(f"E{len(marc) + celda_inicio}", round(insert.total_seconds() / 60, 2))

            celda_inicio = celda_inicio + len(marc) + 1
