from odoo import fields, models, api


class Citas(models.Model):
    _name = 'medical.citas'
    _description = 'Cita Médica'

    name = fields.Char(string="Asunto")
    date_start = fields.Datetime(string='Fecha', required=True)
    date_stop = fields.Datetime(string='Fecha Fin', required=False)
    paciente_id = fields.Many2one(comodel_name='medical.paciente', string='Paciente', required=True)



class Horario(models.Model):
    _name = 'medical.horario'
    _description = 'Horario'

    name = fields.Char(default="Horario de Atención")
    hora_inicio_1 = fields.Float(required=False)
    hora_fin_1 = fields.Float(required=False)
    hora_inicio_2 = fields.Float(required=False)
    hora_fin_2 = fields.Float(required=False)
