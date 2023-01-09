from odoo import fields, models, api


class Empleado(models.Model):
    _inherit = 'hr.employee'

    permisos_id = fields.One2many(comodel_name='racetime.permisos', inverse_name='empleado_id', string='Permisos',
                                  required=False)

    vacaciones_id = fields.One2many(comodel_name='racetime.vacaciones', inverse_name='empleado_id', string='Vacaciones',
                                    required=False)
