from odoo import fields, models, api


class Etapaspostulacion(models.Model):
    _name = 'recruit.etapaspostulaciones'
    _description = 'Description'

    name = fields.Integer(string='Etapa', required=False)



