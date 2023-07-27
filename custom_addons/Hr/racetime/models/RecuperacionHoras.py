from odoo import fields, models, api


class Asignaturas(models.Model):
    _name = 'racetime.asignaturas'
    _description = 'Asignaturas'

    name = fields.Char(string='Asignatura', required=True)


class RecuperacionHoras(models.Model):
    _name = 'racetime.recuperacion_horas'
    _description = 'Recuperación Horas'

    name = fields.Char(related='empleado_id.name')

    fecha_envio_correo = fields.Date(string='Fecha Envío Correo', required=False)
    asignatura_id = fields.Many2one(comodel_name='racetime.asignaturas', string='Asignatura', required=True)
    paralelo = fields.Char(string='Paralelo', required=False)
    novedad = fields.Text(string="Novedad", required=True)
    estado = fields.Selection(string='Estado', selection=[('p', 'PENDIENTE'), ('a', 'APROBADO'), ], default='p', )
    active = fields.Boolean(string='Active', required=False, default=True)
    desde = fields.Datetime(string='Desde', required=True)
    hasta = fields.Datetime(string='Hasta', required=True)
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=True)
    fecha_inasistencia = fields.Date(string='Fecha Inasistencia', required=False)
    marcacion_id = fields.Many2one(comodel_name='racetime.reporte_marcaciones', string='Marcacion',
                                   required=True,
                                   domain="[('empleado_id', '=', empleado_id),('observacion','=','sin_marcacion'),('fecha','=',fecha_inasistencia)]")
