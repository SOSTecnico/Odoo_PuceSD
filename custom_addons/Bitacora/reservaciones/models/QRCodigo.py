from odoo import fields, models, api


class CodigoQR(models.TransientModel):
    _name = 'reservaciones.codigo_qr'
    _description = 'QR Código'

    name = fields.Char()
    usuario_id = fields.Many2one(comodel_name='reservaciones.usuarios', string='Usuario', required=False)
    fecha = fields.Datetime(string='Fecha', required=False)
    codigo_qr = fields.Binary(string="QRCode")
    laboratorio = fields.Char(string='Laboratorio', required=False)
