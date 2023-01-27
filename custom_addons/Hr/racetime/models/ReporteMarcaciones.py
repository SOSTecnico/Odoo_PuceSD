from odoo import fields, models, api


class ReporteMarcacionesWizard(models.TransientModel):
    _name = 'racetime.calculo_marcaciones'
    _description = 'Reporte de Marcación'

    name = fields.Char()
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True)
    empleados_ids = fields.Many2many(comodel_name='hr.employee', string='Empleados')

    def prueba(self):
        print("hello")

class ReporteMarcaciones(models.Model):
    _name = 'racetime.reporte_marcaciones'
    _description = 'Reporte Marcaciones'

    name = fields.Char()
    marcacion_id = fields.Many2one(comodel_name='racetime.detalle_marcacion', string='Marcación', required=False)
    diferencia = fields.Float(string='Diferencia', required=False)
    observacion = fields.Selection(string='Observación', required=False,
                                   selection=[('atraso', 'ATRASO'), ('adelanto', 'ADELANTO'), ], )
    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado',
        required=False)