import pytz

from odoo import fields, models, api


class Citas(models.Model):
    _name = 'medical.citas'
    _description = 'Cita Médica'

    name = fields.Char(string="Asunto")
    date_start = fields.Datetime(string='Fecha', required=True)
    date_stop = fields.Datetime(string='Fecha Fin', required=False)
    paciente_id = fields.Many2one(comodel_name='medical.paciente', string='Paciente', required=False)
    paciente = fields.Char(string="Nombre")

    hora_inicio = fields.Char(compute='compute_fecha_inicio')
    hora_fin = fields.Char(compute='compute_fecha_inicio')

    estado = fields.Selection(string='Estado', default='pendiente',
                              selection=[('pendiente', 'PENDIENTE'), ('no_asiste', 'NO ASISTE'),
                                         ('atendido', 'ATENDIDO'), ])

    @api.depends('date_start', 'date_stop')
    def compute_fecha_inicio(self):
        for rec in self:
            rec.hora_inicio = rec.date_start.astimezone(pytz.timezone('America/Guayaquil')).strftime('%H:%M')
            rec.hora_fin = rec.date_stop.astimezone(pytz.timezone('America/Guayaquil')).strftime('%H:%M')

    @api.onchange('paciente_id')
    def onchange_paciente_id(self):
        for rec in self:
            rec.paciente = rec.paciente_id.name
            rec.name = rec.paciente_id.name


class Horario(models.Model):
    _name = 'medical.horario'
    _description = 'Horario'

    name = fields.Char(default="Horario de Atención")
    hora_inicio_1 = fields.Float(required=False)
    hora_fin_1 = fields.Float(required=False)
    hora_inicio_2 = fields.Float(required=False)
    hora_fin_2 = fields.Float(required=False)
    dias = fields.Many2many(comodel_name='medical.dias', string='Días')


class Dias(models.Model):
    _name = 'medical.dias'
    _description = 'Dias'

    name = fields.Char(string='Día', required=False)
