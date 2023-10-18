from odoo import fields, models, api


class etapas_postulacion(models.Model):
    _name = 'recruit.etapas_postulaciones'
    _description = 'Description'

    name = fields.Integer(string='Etapa', required=False)



