from odoo import fields, models, api

class DescripcionRubros(models.Model):
    _name = 'rolpago.descripcion_rubros'
    _description = 'Description Rubros'

    name = fields.Char()

    tipo_rubro = fields.Selection(string="Tipo de Rubro",
                                    selection=[("I", "INGRESO"), ("D", "EGRESO"), ("P", "PATRIMONIO")],
                                    required=True)




