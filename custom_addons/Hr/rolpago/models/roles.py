from odoo import fields, models, api


class roles(models.Model):
    _name = 'rolpago.roles'
    _description = 'Roles'

    name = fields.Char()

    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado_id',
        required=False)

    periodo = fields.Char(
        string='Periodo',
        required=False)

    rubros_id = fields.One2many(
        comodel_name='rolpago.rubros',
        inverse_name='roles_id',
        string='Rubros_id',
        required=False)
