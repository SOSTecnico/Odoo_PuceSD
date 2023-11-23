from odoo import fields, models, api


class Evidencias(models.Model):
    _name = 'recruit.evidencias'
    _description = 'Description'

    name = fields.Char()

    evidencia = fields.Char(string="Evidencias")
    archivo = fields.Binary(string="Archivo pdf(10mb)")
