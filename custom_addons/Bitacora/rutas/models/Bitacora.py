from odoo import fields, models, api


class Bitacora(models.Model):
    _name = 'rutas.bitacora'
    _description = 'Rutas: Bitácora'

    name = fields.Char()
    usuario_id = fields.Many2one(comodel_name='rutas.usuarios', string='Usuario', required=False)
    bus_id = fields.Many2one(comodel_name='rutas.buses', string='Bus', required=False)
    ruta_id = fields.Many2one(comodel_name='rutas.rutas', string='Ruta', required=False)
    fecha_hora = fields.Datetime(string='Fecha y Hora', required=False)

