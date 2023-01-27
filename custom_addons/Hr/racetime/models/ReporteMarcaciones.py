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
        fecha_ = self.fecha_inicio
        horarios = self.env['racetime.horarios'].sudo().search([])
        if not horarios:
            raise ValidationError('Para realizar los cálculos por favor debe existir al menos un horario disponible')
        while fecha_ <= self.fecha_fin:
            for empleado in self.empleados_ids:
                marcaciones_empleado = self.env['racetime.detalle_marcacion'].sudo().search(
                    [('emp_code', '=', empleado.emp_code), ('fecha_hora', '>=', fecha_),
                     ('fecha_hora', '<=', fecha_)], order="fecha_hora asc")

                # Horarios disponibles de cada empleado
                horarios_empleado = horarios.search_read([('empleados_ids', 'in', empleado.id)])
                print(horarios_empleado)

                for m in marcaciones_empleado:
                    # Comparar las horas con los horarios
                    pass
                    # print(m.fecha_hora)
            fecha_ = fecha_ + timedelta(days=1)

        return


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
