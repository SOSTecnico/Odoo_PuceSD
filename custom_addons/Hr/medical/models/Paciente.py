from odoo import fields, models, api
from datetime import datetime


class Paciente(models.Model):
    _name = 'medical.paciente'
    _description = 'Paciente'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute='_compute_name', store=True, string="Nombre Completo")

    nombres = fields.Char(string='Nombres', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos', required=True, tracking=True)
    cedula = fields.Char(string='Cédula', required=True, tracking=True)
    edad = fields.Integer(string='Edad', required=True)
    email = fields.Char(string='Email', required=False, tracking=True)
    celular = fields.Char(string='Celular', required=False, tracking=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento', required=False)

    contacto_emergencia_id = fields.Many2one(comodel_name='medical.contacto_emergencia',
                                             string='Contacto de Emergencia',
                                             required=False)

    genero = fields.Selection(string='Genero', selection=[('m', 'Masculino'), ('f', 'Femenino'), ('o', 'Otros')],
                              required=True)

    tipo_sangre = fields.Selection(required=True, string='Tipo de Sangre',
                                   selection=[('o_positivo', 'O+'),
                                              ('o_negativo', 'O-'),
                                              ('a_positivo', 'A+'),
                                              ('a_negativo', 'A-'),
                                              ('ab_positivo', 'AB+'),
                                              ('ab_negativo', 'AB-'),
                                              ])

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado Relacionado', required=False)
    categoria_empleado = fields.Many2many(comodel_name='hr.employee.category', string='Categoría',
                                          related='empleado_id.category_ids')
    cargo_empleado = fields.Many2one(comodel_name='hr.job', string='Cargo', required=False,
                                     related='empleado_id.job_id', store=True)

    estudiante_id = fields.Many2one(comodel_name='estudiantes.estudiantes', string='Estudiante', required=False)
    carrera_estudiante = fields.Many2one(comodel_name='estudiantes.carreras', string='Carrera',
                                         related='estudiante_id.carrera_id', store=True)

    active = fields.Boolean(string='Active', required=False, default=True)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for paciente in self:
            paciente.name = f"{paciente.nombres} {paciente.apellidos}"

    @api.onchange('fecha_nacimiento')
    def _onchange_nacimiento(self):
        if self.fecha_nacimiento:
            self.edad = datetime.now().year - self.fecha_nacimiento.year


class ContactoEmergencia(models.Model):
    _name = 'medical.contacto_emergencia'
    _description = 'Contacto Emergencia'

    name = fields.Char(string="Nombre", required=True)
    celular = fields.Char(string='Celular', required=True)
    active = fields.Boolean(string='Active', required=False, default=True)
