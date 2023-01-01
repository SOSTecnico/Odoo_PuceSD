from odoo import fields, models, api


class WifiConfig(models.Model):
    _name = 'wifi.configuracion'
    _description = 'Wifi Configuración'

    name = fields.Char(string="Identificador")
    value = fields.Char(string="Valor", required=True)
    clave = fields.Char(string='Clave', required=True)
