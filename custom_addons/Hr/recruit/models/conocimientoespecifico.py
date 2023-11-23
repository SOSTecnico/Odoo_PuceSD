from odoo import fields, models, api


class Conocimientoespecifico(models.Model):
    _name = 'recruit.conocimientoespecifico'
    _description = 'Description'

    name = fields.Char(string="Conociiento Específico")
