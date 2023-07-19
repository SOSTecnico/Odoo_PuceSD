import pytz

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
    _order = 'fecha desc'

    name = fields.Char(string='Historia Clínica', related='historia_id.name')

    fecha = fields.Date(string='Fecha', required=True,
                        default=lambda self: datetime.now(pytz.timezone('America/Guayaquil')), tracking=True)
    motivo = fields.Text(string="Motivo", required=True, tracking=True)
    diagnostico = fields.Text(string="Diagnóstico", required=False, tracking=True)
    indicaciones = fields.Text(string="Indicaciones", required=False, tracking=True)

    historia_id = fields.Many2one(comodel_name='medical.historia', string='Historia Clínica', required=False,
                                  tracking=True,
                                  ondelete='cascade')
    paciente = fields.Char(string='Paciente', related='historia_id.paciente_id.name')


class HistoriaClinica(models.Model):
    _name = 'medical.historia'
    _description = 'Historia Clínica'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    def _codigo_historia(self):
        ultima_historia = self.search([], order='codigo desc', limit=1)
        if not ultima_historia:
            return 1
        else:
            return ultima_historia.codigo + 1

    def _codigo_str_historia(self):
        ultima_historia = self.search([], order='codigo desc', limit=1)
        return f"H-{str(ultima_historia.codigo + 1).zfill(5)}"

    name = fields.Char(string='Código', default=_codigo_str_historia)
    codigo = fields.Integer(string='Codigo', required=False, default=_codigo_historia)

    paciente_id = fields.Many2one(comodel_name='medical.paciente', string='Paciente', required=True, tracking=True)
    paciente_cedula = fields.Char(string='Paciente Cedula', related='paciente_id.cedula', store=True)
    antecedentes = fields.Text(string="Antecedentes personales", required=False, tracking=True)
    alergias_id = fields.Many2many(comodel_name='medical.alergias', string='Alergias', tracking=True)
    consultas = fields.One2many(comodel_name='medical.consulta', inverse_name='historia_id', string='Consultas',
                                required=False, tracking=True)

    active = fields.Boolean(string='Active', required=False, default=True)

    # def name_get(self):
    #     result = []
    #
    #     for rec in self:
    #         result.append((rec.id, '%s - %s - %s' % (rec.name, rec.paciente_cedula,rec.paciente_id.name)))
    #
    #     return result
