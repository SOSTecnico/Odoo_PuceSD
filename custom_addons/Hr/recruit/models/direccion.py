from odoo import fields, models, api


class Direccion(models.Model):
    _name = 'recruit.direccion'
    _description = 'Description'

    name = fields.Char()

    direccion = fields.Char(string="Direccion")
    calle_principal = fields.Char(string="Calle Principal")
    calle_secundaria = fields.Char(string="Calle Secundaria")
    referencia = fields.Char(string="Referencia")

