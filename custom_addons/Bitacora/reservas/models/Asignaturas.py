from odoo import models, fields


class Asignatura(models.Model):
    _name = 'reservas.asignaturas'
    _description = 'Reserva: Asignatura'

    asignatura = fields.Char(string='Asignatura', required=True)
