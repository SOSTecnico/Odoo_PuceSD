from odoo import fields, models, api



class asignaturas(models.Model):
    _name = 'reservas.asignatura'
    _description = 'asignatura'

    materia = fields.Char(string='Asignaturas')

