from odoo import fields, models, api


class Empleado(models.Model):
    _inherit = 'hr.employee'
    _description = 'Description'

    codigo_sap = fields.Char(
        string='Codigo_sap', 
        required=False)
