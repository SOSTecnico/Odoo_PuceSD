from datetime import datetime

from odoo import fields, models, api


class Transferencia(models.Model):
    _name = 'transferencias.transferencias'
    _description = 'Transferencia'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'codigo'
    _sql_constraints = [
        ('codigo_transferencia', 'unique(codigo)', 'Ya existe una Transferencia con el código que intenta ingresar')]

    fecha = fields.Date(string='Fecha', required=True, default=lambda self: datetime.now(), tracking=True,
                        track_visibility='onchange')
    codigo = fields.Char(string='Código', required=True, tracking=True, track_visibility='onchange')

    custodio_origen_id = fields.Many2one(comodel_name='hr.employee', string='Custodio Origen', required=True,
                                         tracking=True, track_visibility='onchange')

    custodio_destino_id = fields.Many2one(comodel_name='hr.employee', string='Custodio Destino', required=True,
                                          tracking=True, track_visibility='onchange')

    ubicacion_origen_id = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Ubicación Origen',
                                          required=True, tracking=True, track_visibility='onchange')

    ubicacion_destino = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Ubicación Destino',
                                        required=True, tracking=True, track_visibility='onchange')

    activos_ids = fields.Many2many(comodel_name='transferencias.activos', string='Activos', required=True)

    archivo = fields.Binary(string="Evidencia Digital")
