from odoo import fields, models, api


class DetalleRequerimiento(models.Model):
    _name = 'reservaciones.detalle_requerimientos'
    _description = 'Detalle Requerimiento'

    name = fields.Char(string="Descripción")


class Requerimiento(models.Model):
    _name = 'reservas.requerimientos'
    _description = 'Requerimiento'

    name = fields.Char()
    detalle_requerimiento_id = fields.Many2one(comodel_name='reservaciones.detalle_requerimientos',
                                               string='Detalle Requerimiento', required=True)
