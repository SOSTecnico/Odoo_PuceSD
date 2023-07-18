from odoo import fields, models, api

from datetime import datetime


class Alergias(models.Model):
    _name = 'medical.alergias'
    _description = 'Alergias'

    name = fields.Char(string='Alergia', required=True)


class Consulta(models.Model):
    _name = 'medical.consulta'
    _description = 'Consulta'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()

    fecha = fields.Date(string='Fecha', required=True, default=lambda self: datetime.now(), tracking=True)
    motivo = fields.Text(string="Motivo", required=False, tracking=True)
    diagnostico = fields.Text(string="Diagnóstico", required=False, tracking=True)

    historia_id = fields.Many2one(comodel_name='medical.historia', string='Historia_id', required=False, tracking=True)


class HistoriaClinica(models.Model):
    _name = 'medical.historia'
    _description = 'Historia Clínica'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Código')
    paciente_id = fields.Many2one(comodel_name='medical.paciente', string='Paciente', required=True, tracking=True)
    antecedentes = fields.Text(string="Antecedentes personales de Salud", required=False, tracking=True)
    alergias_id = fields.Many2many(comodel_name='medical.alergias', string='Alergias', tracking=True)
    consultas = fields.One2many(comodel_name='medical.consulta', inverse_name='historia_id', string='Consultas',
                                required=False, tracking=True)
