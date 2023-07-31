from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'racetime.asistencia_virtual'
    _description = 'Asistencia Virtual'

    name = fields.Char()

    fecha = fields.Datetime(string='Fecha', required=False)
    correo = fields.Char(string='Correo', required=True)
    nombres = fields.Char(string='Nombres', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    actividad = fields.Selection(string='Actividad', required=True,
                                 selection=[('cd', 'Clases y Actividades de Docencia'),
                                            ('d', 'Actividades de Docencia'),
                                            ('c', 'Solo Clases'),
                                            ], )
    programa = fields.Selection(string='Programa', selection=[('g', 'Grado'), ('p', 'Posgrado'), ('tec', 'Pucetec')],
                                required=True, )
    carrera_id = fields.Many2one(comodel_name='estudiantes.carreras', string='Carrera', required=True)
    asignatura_id = fields.Many2one(comodel_name='racetime.asignaturas', string='Asignatura', required=False)

    def _niveles(self):
        niveles = []
        for i in range(7):
            niveles.append((i, i))
        return niveles

    Nivel = fields.Selection(string='Nivel', selection=_niveles, required=True, )

    def _paralelo(self):
        paralelos = []
        for i in range(65,80):
            pass
    