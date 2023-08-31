from odoo import fields, models, api


class Visitante(models.Model):
    _name = 'visitas.visitantes'
    _description = 'Visitante'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nombre Completo", compute="_compute_name", store=True, )
    active = fields.Boolean(string='Active', required=False, default=True)

    nombres = fields.Char(string='Nombres', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    cedula = fields.Char(string='Cédula')
    correo = fields.Char(string='Correo')

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for usuario in self:
            usuario.name = f"{usuario.nombres} {usuario.apellidos}"
