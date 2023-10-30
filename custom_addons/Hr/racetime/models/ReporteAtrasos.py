import xlsxwriter

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
        print('Hellou Madafaka!!!')
        print(data)

        # Empezar a Generar el Reporte desde Aqui
        sheet = workbook.add_worksheet("Reporte de Atrasos")
        sheet.write("A2", "Que más ve!!!")
