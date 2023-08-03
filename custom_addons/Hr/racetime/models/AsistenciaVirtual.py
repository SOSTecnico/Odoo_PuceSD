from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'racetime.asistencia_virtual'
    _description = 'Asistencia Virtual'

    name = fields.Char(string='Nombre', compute='_compute_name', store=True)

    fecha = fields.Date(string='Fecha', required=False)
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
    carrera_id = fields.Many2one(comodel_name='estudiantes.carreras', string='Carrera', required=True,
                                 domain="[('parent_id','!=',False),('name','!=','MAESTRÍAS'),('name','!=','ESPECIALIDADES')]")
    asignatura_id = fields.Many2one(comodel_name='racetime.asignaturas', string='Asignatura', required=False)

    def _niveles(self):
        niveles = []
        for i in range(1, 11):
            niveles.append((f"{i}", i))
        return niveles

    nivel = fields.Selection(string='Nivel', selection=_niveles, required=True, )

    def _paralelo(self):
        paralelos = []
        for i in range(65, 80):
            paralelos.append((chr(i), chr(i)))
        return paralelos

    paralelo = fields.Selection(string='Paralelo', selection=_paralelo, required=True, default='A')

    inquietud = fields.Boolean(string='Inquietud', required=False)
    problemas_tecnicos = fields.Boolean(string='Problemas Técnicos', required=False)

    problemas_tecnicos_desc = fields.Text(string="Descripción Problemas Técnicos", required=False)

    espacios_dialogo = fields.Boolean(string='Espacios de Díalogo', required=False)

    motivacion_asignatura = fields.Boolean(string='Motivación Asignatura', required=False)

    aportes_clase = fields.Char(string='Aportes de la Clase', required=False)
    actividades_academicas = fields.Boolean(string='Actividades ', required=False)
    actividades_academicas_detalle = fields.Text(string="Actividades Detalle", required=False)
    novedades_estudiantes = fields.Text(string="Novedades Estudiantes", required=False)
    sugerencias = fields.Text(string="Sugerencias", required=False)

    hora_inicio = fields.Datetime(string='Hora de Inicio', required=True)
    hora_fin = fields.Datetime(string='Hora de Fin', required=True)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.nombres} {rec.apellidos}"
