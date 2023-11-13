from odoo import fields, models, api


class Usuario(models.Model):
    _name = 'rutas.usuarios'
    _description = 'Rutas: Usuario'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre Completo', compute='_compute_name', store=True)
    nombres = fields.Char(string='Nombres', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos', required=True, tracking=True)
    cedula = fields.Char(string='Cédula', required=True,tracking=True)
    correo = fields.Char(string='Correo', required=True,tracking=True)
    active = fields.Boolean(string='Active', required=False, default=True)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for usuario in self:
            usuario.name = f"{usuario.nombres} {usuario.apellidos}"
