from odoo import models, fields


class Asignatura(models.Model):
    _name = 'reservas.asignaturas'
    _description = 'Reserva: Asignatura'
    _rec_name = "asignatura"

    asignatura = fields.Char(string='Asignatura', required=True)
