import pytz

from odoo import fields, models, api

from datetime import datetime, timedelta


class Alergias(models.Model):
    _name = 'medical.alergias'
    _description = 'Alergias'

    name = fields.Char(string='Alergia', required=True)


class Consulta(models.Model):
    _name = 'medical.consulta'
    _description = 'Consulta'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha desc'

    name = fields.Char(string='Historia', related='historia_id.name')
    active = fields.Boolean(string='Active', required=False, default=True)
    fecha = fields.Date(string='Fecha', required=True,
                        default=lambda self: datetime.now(pytz.timezone('America/Guayaquil')), tracking=True)

    # Se agrega campo Hora para estadisticas

    def _default_hora(self):
        minuto = datetime.now().minute
        hora = datetime.now().hour
        tiempo = timedelta(hours=(hora - 5), minutes=minuto)
        return tiempo.total_seconds() / 60 / 60

    hora = fields.Float(string='Hora', default=_default_hora)
    motivo = fields.Text(string="Motivo", required=True, tracking=True)
    enfermedad_actual = fields.Text(string="Enfermedad Actual", required=False)
    diagnostico = fields.Text(string="Diagnóstico", required=False, tracking=True)
    examen_fisico = fields.Text(string="Examen Fisico", required=False, tracking=True)
    indicaciones = fields.Text(string="Indicaciones", required=False, tracking=True)

    historia_id = fields.Many2one(comodel_name='medical.historia', string='Historia Clínica', required=False,
                                  tracking=True, ondelete='cascade')
    paciente = fields.Char(string='Paciente', related='historia_id.paciente_id.name')

    # Signos Vitales

    temperatura = fields.Integer(string='Temperatura', required=False)
    presion_arterial = fields.Char(string='Presión Arterial', required=False)
    pulso = fields.Integer(string='Pulso', required=False)
    frecuencia_respiratoria = fields.Integer(string='Frecuencia Respiratoria', required=False)
    peso = fields.Integer(string='Peso', required=False)
    talla = fields.Integer(string='Talla', required=False)
    imc = fields.Float(string='IMC', required=False, digits=(3, 1))
    imc_detalle = fields.Char(string='Resultado IMC', required=False)

    cie_10 = fields.Many2one(comodel_name='medical.cie10', string='CIE 10', required=False)

    @api.onchange('imc')
    def _resultado_imc(self):
        for rec in self:

            if rec.imc == 0:
                rec.imc_detalle = ''
                return

            if rec.imc < 18.5:
                rec.imc_detalle = 'Bajo peso'
            elif rec.imc >= 18.5 and rec.imc <= 24.9:
                rec.imc_detalle = 'Normal'
            elif rec.imc >= 25 and rec.imc <= 29.9:
                rec.imc_detalle = 'Sobrepeso'
            elif rec.imc >= 30:
                rec.imc_detalle = 'Obesidad'

    @api.onchange('talla', 'peso')
    def _onchange_imc(self):
        if self.peso and self.talla:
            self.imc = self.peso / ((self.talla / 100) ** 2)

    perimetro_abdominal = fields.Integer(string='Perímetro Abdominal', required=False)
    pulsioximetria = fields.Integer(string='Pulsioximetria', required=False)

    certificado = fields.Binary(string="", )
    certificado_name = fields.Char(string='Certificado Médico', required=False)


class HistoriaClinica(models.Model):
    _name = 'medical.historia'
    _description = 'Historia Clínica'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    def _codigo_historia(self):
        ultima_historia = self.search(['|', ('active', '=', True), ('active', '=', False)], order='codigo desc',
                                      limit=1)
        if not ultima_historia:
            return 1
        else:
            return ultima_historia.codigo + 1

    def _codigo_str_historia(self):
        ultima_historia = self.search(['|', ('active', '=', True), ('active', '=', False)], order='codigo desc',
                                      limit=1)
        return f"H-{str(ultima_historia.codigo + 1).zfill(5)}"

    name = fields.Char(string='Código', default=_codigo_str_historia)
    codigo = fields.Integer(string='_codigo', required=False, default=_codigo_historia)

    paciente_id = fields.Many2one(comodel_name='medical.paciente', string='Paciente', required=True, tracking=True)
    paciente_cedula = fields.Char(string='Paciente Cedula', related='paciente_id.cedula')

    empleado = fields.Many2one(comodel_name='hr.employee', string='Empleado', related='paciente_id.empleado_id')
    categoria_empleado = fields.Many2many(comodel_name='hr.employee.category', string='Categoría',
                                          related='paciente_id.empleado_id.category_ids')

    estudiante = fields.Many2one(comodel_name='estudiantes.estudiantes', string='Estudiante', required=False,
                                 related='paciente_id.estudiante_id')
    carrera_estudiante = fields.Many2one(comodel_name='estudiantes.carreras', string='Carrera Estudiante',
                                         related='paciente_id.estudiante_id.carrera_id', store=True)

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
