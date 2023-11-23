from odoo import fields, models, api


class Habilidades(models.Model):
    _name = 'recruit.habilidades'
    _description = 'Description'

    name = fields.Char(string='Habilidad')
