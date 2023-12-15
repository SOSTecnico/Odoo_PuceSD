from odoo import fields, models, api


class Laboratorio(models.Model):
    _name = 'reservas.laboratorios'
    _description = 'Reservas: Laboratorio'

    name = fields.Char(string='Laboratorio', required=True)
    referencia = fields.Char(string='Referencia', required=False)
    capacidad = fields.Integer(string='Capacidad', required=True)
    detalle_programas_id = fields.One2many(comodel_name='reservas.laboratorio_programa', inverse_name='laboratorio_id',
                                           string='Programas', required=False)


class Programas(models.Model):
    _name = 'reservas.programas'
    _description = 'Reservas: Programa'

    name = fields.Char()


class LaboratorioProgramas(models.Model):
    _name = 'reservas.laboratorio_programa'
    _description = 'LaboratorioProgramas'
    _order = 'periodo desc'

    periodo = fields.Char(string='Periodo', required=True)
    laboratorio_id = fields.Many2one(comodel_name='reservas.laboratorios', string='Laboratorio', required=False)
    programas_ids = fields.Many2many(comodel_name='reservas.programas', string='Programas')
