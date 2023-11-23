from odoo import fields, models, api


class Actividades(models.Model):
    _name = 'recruit.actividades'
    _description = 'Description'

    name = fields.Char(string="Actividades")
