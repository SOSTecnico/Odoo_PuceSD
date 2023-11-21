from odoo import fields, models, api


class Carrera(models.Model):
    _name = 'enfermeria.carreras'
    _description = 'Enfermería: Carrera'

    name = fields.Char(string="Carrera")


class Asignatura(models.Model):
    _name = 'enfermeria.asignaturas'
    _description = 'Enfermería: Asignatura'

    name = fields.Char(string="Asignatura")


class Laboratorio(models.Model):
    _name = 'enfermeria.laboratorios'
    _description = 'Enfermería: Laboratorio'

    name = fields.Char(string="Laboratorio")


class Registro(models.Model):
    _name = 'enfermeria.registros'
    _description = 'Registro'

    _rec_name = 'estudiante_id'

    estudiante_id = fields.Many2one(comodel_name='estudiantes.estudiantes', string='Estudiante', required=False)
    carrera_id = fields.Many2one(comodel_name='enfermeria.carreras', string='Carrera', required=False)
    asignatura_id = fields.Many2one(comodel_name='enfermeria.asignaturas', string='Asignatura', required=False)
    nivel = fields.Char(string='Nivel', required=False)
    paralelo = fields.Char(string='Paralelo', required=False)
    laboratorio_id = fields.Many2one(comodel_name='enfermeria.laboratorios', string='Laboratorio', required=False)
    tema = fields.Text(string="Tema de Práctica", required=False)
    fecha = fields.Date(string='Fecha', required=False)
    hora_inicio = fields.Datetime(string='Hora de Inicio', required=False)
    hora_fin = fields.Datetime(string='Hora Fin', required=False)
