from odoo import fields, models, api


class Discapacidad(models.Model):
    _name = 'recruit.discapacidad'
    _description = 'Description'

    _rec_name = 'tipo_discapacidad'

    tipo_discapacidad = fields.Char(string='Tipo de discapacidad', required=False)
    porcentaje_discapacidad = fields.Integer(string='Porcentaje de discapacidad', required=False)
