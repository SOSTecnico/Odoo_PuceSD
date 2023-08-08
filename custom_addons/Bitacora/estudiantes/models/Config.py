from odoo import fields, models, api


class Config(models.Model):
    _name = 'estudiantes.config'
    _description = 'Configuración'

    name = fields.Char(string="Nombre", required=True)
    key = fields.Char(string='Clave', required=True)
    value = fields.Char(string='Valor', required=True)



