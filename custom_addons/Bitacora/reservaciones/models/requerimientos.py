from odoo import fields, models, api


class DetalleRequerimiento(models.Model):
    _name = 'reservaciones.detalle_req'
    _description = 'Detalle Requerimiento'

    name = fields.Char(string="Descripción")


class Requerimiento(models.Model):
    _name = 'reservaciones.req'
    _description = 'Requerimiento'

    name = fields.Char()

    det_req_id = fields.Many2many(comodel_name='reservaciones.detalle_req',
                                               string='Detalle Requerimiento', required=True)

    recurso_id = fields.Many2one(
        comodel_name='reservaciones.recursos',
        string='Recurso',
        required=False)