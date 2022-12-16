from odoo import fields, models, api


class Recurso(models.Model):
    _name = 'reservaciones.recursos'
    _description = 'Recurso'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Recurso", required=True, tracking=True)
    capacidad = fields.Integer(string='Capacidad', required=False)
    disponible = fields.Integer(string='Disponible', required=False)
    observaciones = fields.Text(string="Observaciones", required=False)

    requerimientos_id = fields.One2many(
        comodel_name='reservaciones.req',
        inverse_name='recurso_id',
        string='Requerimientos',
        required=False,tracking=True)