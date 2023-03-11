import json

from odoo import fields, models, api
from datetime import timedelta, datetime

from odoo.exceptions import ValidationError


class Dias(models.Model):
    _name = 'racetime.dias'
    _description = 'Dias'

    name = fields.Char()


class Horarios(models.Model):
    _name = 'racetime.horarios'
    _description = 'Horarios'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(string="Nombre", required=False, compute='_horario_name', store=True)
    # fecha_inicio = fields.Date(string='Fecha Inicio', required=True, tracking=True)
    # fecha_fin = fields.Date(string='Fecha Fin', required=False, tracking=True)
    active = fields.Boolean(string='Active', required=False, default=True, tracking=True)
    # empleados_ids = fields.Many2many(comodel_name='hr.employee', string='Empleados')
    detalle_horario_id = fields.One2many(comodel_name='racetime.detalle_horarios', inverse_name='horario_id',
                                         string='Detalle de Horario', required=False)
    total_horas = fields.Float(string='Total Horas', required=False, default=0)
    horas = fields.Float(string='Total Horas', required=False, related='total_horas', readonly=True)

    @api.constrains('total_horas')
    def check_total_horas(self):
        for rec in self:
            if rec.total_horas < 40 or rec.total_horas > 40:
                raise ValidationError('Favor de revisar el total de horas')

    @api.onchange('detalle_horario_id')
    def onchange_detalle_horario(self):
        res = 0
        for horario in self.detalle_horario_id:
            for dia in horario.dias:
                marcacion_1 = timedelta(seconds=0)
                if horario.marcacion_1 > 0:
                    marcacion_1 = timedelta(hours=horario.marcacion_1)
                marcacion_2 = timedelta(seconds=0)
                if horario.marcacion_2 > 0:
                    marcacion_2 = timedelta(hours=horario.marcacion_2)
                marcacion_3 = timedelta(seconds=0)
                if horario.marcacion_3 > 0:
                    marcacion_3 = timedelta(hours=horario.marcacion_3)
                marcacion_4 = timedelta(seconds=0)
                if horario.marcacion_4 > 0:
                    marcacion_4 = timedelta(hours=horario.marcacion_4)

                if marcacion_1.total_seconds() > 0 and marcacion_2.total_seconds() > 0:
                    res = res + ((marcacion_2 - marcacion_1).total_seconds() / 60) / 60

                if marcacion_3.total_seconds() > 0 and marcacion_4.total_seconds() > 0:
                    res = res + ((marcacion_4 - marcacion_3).total_seconds() / 60) / 60

        self.total_horas = res

    @api.depends('detalle_horario_id')
    def _horario_name(self):
        for rec in self:
            m_1 = (datetime.min + timedelta(hours=rec.detalle_horario_id.marcacion_1)).strftime("%H:%M")
            m_2 = (datetime.min + timedelta(hours=rec.detalle_horario_id.marcacion_2)).strftime("%H:%M")
            m_3 = (datetime.min + timedelta(hours=rec.detalle_horario_id.marcacion_3)).strftime("%H:%M")
            m_4 = (datetime.min + timedelta(hours=rec.detalle_horario_id.marcacion_4)).strftime("%H:%M")
            rec.name = f"{m_1} - {m_2} || {m_3} - {m_4}"


class DetalleHorarios(models.Model):
    _name = 'racetime.detalle_horarios'
    _description = 'DetalleHorarios'

    name = fields.Char()
    dias = fields.Many2many(comodel_name='racetime.dias', string='Dias')
    marcacion_1 = fields.Float(string='Marcacion Entrada', required=False)
    marcacion_2 = fields.Float(string='Marcacion Salida', required=False)
    marcacion_3 = fields.Float(string='Marcacion Entrada', required=False)
    marcacion_4 = fields.Float(string='Marcacion Salida', required=False)
    horario_id = fields.Many2one(comodel_name='racetime.horarios', string='Horario', required=False)
    total_horas = fields.Float(string='Total Horas', required=False)

    @api.constrains('marcacion_1', 'marcacion_2', 'marcacion_3', 'marcacion_4')
    def check_marcaciones(self):
        for rec in self:
            if rec.marcacion_1 > 0 and rec.marcacion_2 == 0:
                raise ValidationError('La marcacion Salida no puede ser 0')

            if rec.marcacion_3 > 0 and rec.marcacion_4 == 0:
                raise ValidationError('La marcacion Salida no puede ser 0')

            if rec.marcacion_1 == 0 and rec.marcacion_2 == 0 and rec.marcacion_3 == 0 and rec.marcacion_4 == 0:
                raise ValidationError('La marcacion Salida no puede ser 0')


class AsignacionHorario(models.Model):
    _name = 'racetime.asignacion_horario'
    _description = 'Asignación Horario'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleados', tracking=True)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True, tracking=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=False, tracking=True)

    dias = fields.Many2many(comodel_name='racetime.dias', string='Días')
    marcacion_1 = fields.Float(string='Marcacion Entrada', required=False)
    marcacion_2 = fields.Float(string='Marcacion Salida', required=False)
    marcacion_3 = fields.Float(string='Marcacion Entrada', required=False)
    marcacion_4 = fields.Float(string='Marcacion Salida', required=False)

    total_horas = fields.Float(string='Total Horas', required=False)

    horario = fields.Char(string='Horario', required=False, compute='_horario')

    @api.onchange('dias')
    def onchange_detalle_horario(self):
        res = 0
        for dia in self.dias:
            marcacion_1 = timedelta(seconds=0)
            if self.marcacion_1 > 0:
                marcacion_1 = timedelta(hours=self.marcacion_1)
            marcacion_2 = timedelta(seconds=0)
            if self.marcacion_2 > 0:
                marcacion_2 = timedelta(hours=self.marcacion_2)
            marcacion_3 = timedelta(seconds=0)
            if self.marcacion_3 > 0:
                marcacion_3 = timedelta(hours=self.marcacion_3)
            marcacion_4 = timedelta(seconds=0)
            if self.marcacion_4 > 0:
                marcacion_4 = timedelta(hours=self.marcacion_4)

            if marcacion_1.total_seconds() > 0 and marcacion_2.total_seconds() > 0:
                res = res + ((marcacion_2 - marcacion_1).total_seconds() / 60) / 60

            if marcacion_3.total_seconds() > 0 and marcacion_4.total_seconds() > 0:
                res = res + ((marcacion_4 - marcacion_3).total_seconds() / 60) / 60

        self.total_horas = res

    @api.constrains('total_horas')
    def check_total_horas(self):
        for rec in self:
            if rec.total_horas < 40:
                raise ValidationError('Favor de revisar el total de horas')

    @api.depends('marcacion_1', 'marcacion_2', 'marcacion_3', 'marcacion_4')
    def _horario(self):
        for rec in self:
            m_1 = (datetime.min + timedelta(hours=rec.marcacion_1)).strftime("%H:%M")
            m_2 = (datetime.min + timedelta(hours=rec.marcacion_2)).strftime("%H:%M")
            m_3 = (datetime.min + timedelta(hours=rec.marcacion_3)).strftime("%H:%M")
            m_4 = (datetime.min + timedelta(hours=rec.marcacion_4)).strftime("%H:%M")
            rec.horario = f"{m_1} - {m_2} || {m_3} - {m_4}"

    @api.constrains('marcacion_1', 'marcacion_2', 'marcacion_3', 'marcacion_4')
    def check_marcaciones(self):
        for rec in self:
            if rec.marcacion_1 > 0 and rec.marcacion_2 == 0:
                raise ValidationError('La marcacion Salida no puede ser 0')

            if rec.marcacion_3 > 0 and rec.marcacion_4 == 0:
                raise ValidationError('La marcacion Salida no puede ser 0')

            if rec.marcacion_1 == 0 and rec.marcacion_2 == 0 and rec.marcacion_3 == 0 and rec.marcacion_4 == 0:
                raise ValidationError('La marcacion Salida no puede ser 0')



class AsignacionHorarioMultiple(models.TransientModel):
    _name = 'racetime.asignacion_horario_multiple'
    _description = 'AsignacionHorarioMultiple'
    _inherit = 'racetime.asignacion_horario'

    name = fields.Char()
    empleados_ids = fields.Many2many(comodel_name='hr.employee', string='Empleados')

    def generar_horarios(self):
        for empleado in self.empleados_ids:

            self.env['racetime.asignacion_horario'].create({
                'empleado_id': empleado.id,
                'fecha_inicio': self.fecha_inicio,
                'fecha_fin': self.fecha_fin,
                'marcacion_1': self.marcacion_1,
                'marcacion_2': self.marcacion_2,
                'marcacion_3': self.marcacion_3,
                'marcacion_4': self.marcacion_4,
                'dias': self.dias,
                'total_horas': self.total_horas
            })

        return {
            'type': 'tree',
            'name': 'Asignación de Horarios',
            'context': {'search_default_group_empleado': 1},
            'view_mode': 'tree,form',
            'res_model': 'racetime.asignacion_horario',
            'type': 'ir.actions.act_window',
            'target': 'main'
        }
