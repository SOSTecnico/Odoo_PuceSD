from odoo import fields, models, api

from datetime import datetime

class Usuarios(models.Model):
    _name = 'reservaciones.usuarios'
    _description = 'Usuario Laboratorio'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute="_compute_name", store=True, string="Nombre Completo")
    nombres = fields.Char(string='Nombres', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos', required=True, tracking=True)
    cedula = fields.Char(string='Cédula', required=True, tracking=True)
    email = fields.Char(string='Correo', required=False, tracking=True, )
    carrera = fields.Char(string='Carrera', required=False, tracking=True)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for usuario in self:
            usuario.name = f"{usuario.nombres} {usuario.apellidos}"


class Ingresos(models.Model):
    _name = 'reservaciones.ingresos'
    _description = 'Laboratorio Ingresos'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(related='usuario_id.name', store=True)
    fecha = fields.Datetime(string='Fecha', required=True, tracking=True, default=lambda self: datetime.now())
    usuario_id = fields.Many2one(comodel_name='reservaciones.usuarios', string='Usuario', required=True, tracking=True)
    laboratorio = fields.Char(string='Laboratorio', required=False)
    email = fields.Char(
        string='Email',
        required=False, related='usuario_id.email')
    cedula = fields.Char(
        string='Cédula',
        required=False, related='usuario_id.cedula')
    nombres = fields.Char(
        string='Nombres',
        required=False, related='usuario_id.nombres')
    apellidos = fields.Char(
        string='Apellidos',
        required=False, related='usuario_id.apellidos')
    carrera = fields.Char(
        string='Carrera',
        required=False, related='usuario_id.carrera', store=True)
