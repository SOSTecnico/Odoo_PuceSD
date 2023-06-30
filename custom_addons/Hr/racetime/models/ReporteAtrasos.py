from odoo import fields, models, api


class ReporteAtrasos(models.TransientModel):
    _name = 'racetime.reporte_atrasos'
    _description = 'Reporte Atrasos'

    name = fields.Char()

    empleados_id = fields.Many2many(comodel_name='hr.employee', string='Empleados')
    fecha_inicio = fields.Datetime(string='Fecha Inicial', required=True)
    fecha_final = fields.Datetime(string='Fecha Final', required=True)



