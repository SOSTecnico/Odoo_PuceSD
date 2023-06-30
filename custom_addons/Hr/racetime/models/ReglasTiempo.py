from odoo import fields, models, api


class ReglasTiempo(models.Model):
    _name = 'racetime.reglas'
    _description = 'Reglas de Tiempo'

    name = fields.Char()
    tolerancia = fields.Float(string='Tolerancia', required=False, default=0)
    sin_marcacion = fields.Float(string='Tiempo considerado para constar SIN MARCACIÓN', required=False, default=0)

    evaluacion_desemp = fields.Float(string='Evaluación de Desempeño', required=False)

    descuento_rol = fields.Float(string='Descuento al Rol', required=False)