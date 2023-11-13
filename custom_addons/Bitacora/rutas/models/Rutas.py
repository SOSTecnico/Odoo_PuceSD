from odoo import fields, models, api


class Parada(models.Model):
    _name = 'rutas.paradas'
    _description = 'Rutas: Parada'

    name = fields.Char(string='Parada')
    sequence = fields.Integer(default=1)


class Rutas(models.Model):
    _name = 'rutas.rutas'
    _description = 'Rutas: Rutas'

    name = fields.Char(string='Nombre De Ruta')
    buses_id = fields.Many2many(comodel_name='rutas.buses', string='Buses')
    rutas_paradas = fields.One2many(comodel_name='rutas.ruta_parada', inverse_name='ruta_id', string='Paradas',
                                    required=True)
    buses_rutas = fields.One2many(comodel_name='rutas.bus_ruta', inverse_name='ruta_id', string='Estado Rutas')


class RutaParada(models.Model):
    _name = 'rutas.ruta_parada'
    _description = 'RutaParada'

    name = fields.Char()
    ruta_id = fields.Many2one(comodel_name='rutas.rutas', string='Ruta', required=False)
    parada_id = fields.Many2one(comodel_name='rutas.paradas', string='Parada', required=False)
    sequence = fields.Integer(string='Sequence', required=False, default=1)


class BusRuta(models.Model):
    _name = 'rutas.bus_ruta'
    _description = 'Rutas: BusRuta'

    estado = fields.Selection(string='Estado', selection=[('pendiente', 'En Espera'), ('en_ruta', 'En Ruta'), ])
    ruta_id = fields.Many2one(comodel_name='rutas.rutas', string='Ruta')
    bus_id = fields.Many2one(comodel_name='rutas.buses', string='Bus')
