from odoo import models, fields


class asignaturas(models.Model):
    _name = 'reservas.asignaturas'
    _description = 'asignaturas'

    materia = fields.Char(string='Asignaturas')

    asignaturas = fields.Char(string='Codigo de Sala')
    materias = fields.Selection(
        string='Sala',
        selection=[('sala computo 1', 'SALA COMPUTO 1'),
                   ('sala computo 2', 'SALA COMPUTO 2'),
                   ('sala computo 3', 'SALA COMPUTO 3'), ], default='sala computo 1')