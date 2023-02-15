from odoo import fields, models, api


class descripcion_rubros(models.Model):
    _name = 'rolpago.descripcion_rubros'
    _description = 'Description Rubros'

    name = fields.Char()

    roprubroltip = fields.Selection(string="tipo de rubro", selection=[("I", "INGRESO"), ("D", "EGRESO"), ("P", "PATRIMONIO")],
                                    required=True)

    