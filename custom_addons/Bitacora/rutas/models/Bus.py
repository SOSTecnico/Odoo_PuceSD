from odoo import fields, models, api


class Bus(models.Model):
    _name = 'rutas.buses'
    _description = 'Rutas: Bus'

    name = fields.Char(string='Placa')
    chofer_id = fields.Many2one(comodel_name='rutas.choferes', string='Chófer', required=True)
    active = fields.Boolean(string='Active', required=False, default=True)