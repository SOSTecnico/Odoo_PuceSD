from odoo import fields, models, api


class Paciente(models.Model):
    _name = 'medical.paciente'
    _description = 'Paciente'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute='_compute_name', store=True)

    nombres = fields.Char(string='Nombres', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos', required=True, tracking=True)
    cedula = fields.Char(string='Cédula', required=True, tracking=True)
    email = fields.Char(string='Email', required=False, tracking=True)
    celular = fields.Char(string='Celular', required=False, tracking=True)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for paciente in self:
            paciente.name = f"{paciente.nombres} {paciente.apellidos}"
