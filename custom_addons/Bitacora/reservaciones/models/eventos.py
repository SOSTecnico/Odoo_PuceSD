from odoo import fields, models, api


class Evento(models.Model):
    _name = 'reservaciones.eventos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Evento'

    name = fields.Char(string="Evento", tracking=True, required=True)
