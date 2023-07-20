from odoo import fields, models, api


class Carreras(models.Model):
    _name = 'estudiantes.carreras'
    _description = 'Carreras'

    name = fields.Char(string='Carrera', required=True)


class Estudiantes(models.Model):
    _name = 'estudiantes.estudiantes'
    _description = 'Description'
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('cedula','unique(cedula)','Ya existe un estudiante ingresado con esa Cédula!')
    ]

    name = fields.Char(compute='_compute_name', store=True, string="Nombre Completo")

    nombres = fields.Char(string='Nombres', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos', required=True, tracking=True)
    cedula = fields.Char(string='Cédula', required=True, tracking=True)
    correo = fields.Char(string='Correo', required=False, tracking=True)
    celular = fields.Char(string='Celular', required=False, tracking=True)
    carrera_id = fields.Many2one(comodel_name='estudiantes.carreras', string='Carrera', required=True, tracking=True)
    active = fields.Boolean(string='Active', required=False, default=True)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for estudiante in self:
            estudiante.name = f"{estudiante.nombres} {estudiante.apellidos}"
