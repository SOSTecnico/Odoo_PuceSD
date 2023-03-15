import json

from odoo import fields, models, api
from datetime import timedelta, datetime, date

from odoo.exceptions import ValidationError
from odoo.tools import html2plaintext


class Dias(models.Model):
    _name = 'racetime.dias'
    _description = 'Dias'

    name = fields.Char()


class Horarios(models.Model):
    _name = 'racetime.horarios'
    _description = 'Horarios'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(string="Nombre", required=False)
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


class DetalleHorarios(models.Model):
    _name = 'racetime.detalle_horarios'
    _description = 'DetalleHorarios'

    name = fields.Char()
    dias = fields.Many2many(comodel_name='racetime.dias', string='Dias')
    marcacion_1 = fields.Float(string='Entrada', required=False)
    marcacion_2 = fields.Float(string='Salida D', required=False)
    marcacion_3 = fields.Float(string='Entrada D', required=False)
    marcacion_4 = fields.Float(string='Salida', required=False)
    horario_id = fields.Many2one(comodel_name='racetime.horarios', string='Horario', required=False)
    total_horas = fields.Float(string='Total Horas', required=False)

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=False,
                                  related='asignacion_horario_id.empleado_id')
    fecha_inicio = fields.Date(string='Fecha Inicio', required=False, related='asignacion_horario_id.fecha_inicio')
    fecha_fin = fields.Date(string='Fecha Inicio', required=False, related='asignacion_horario_id.fecha_fin')

    asignacion_horario_id = fields.Many2one(comodel_name='racetime.asignacion_horario', string='Asignacion_horario_id',
                                            required=False, ondelete='cascade')

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
    _order = 'fecha_fin desc'

    name = fields.Char()
    horario_ = fields.Text(string='Horario', required=False, compute='_set_name_horario')

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', tracking=True)

    fecha_inicio = fields.Date(string='Fecha Inicio', required=False, tracking=True, copy=False)
    fecha_fin = fields.Date(string='Fecha Fin', required=False, tracking=True, copy=False)

    horario_id = fields.Many2one(comodel_name='racetime.horarios', string='Horario', required=False)

    horario = fields.One2many(comodel_name='racetime.detalle_horarios', inverse_name='asignacion_horario_id',
                              string='Horarios del Empleado', required=False)
    total_horas = fields.Float(string='Total Horas', required=False)

    @api.depends('horario')
    def _set_name_horario(self):
        for rec in self:
            rec.horario_ = ""
            for h in rec.horario:
                m1 = (datetime.min + timedelta(hours=h.marcacion_1)).strftime("%H:%M")
                m2 = (datetime.min + timedelta(hours=h.marcacion_2)).strftime("%H:%M")
                m3 = (datetime.min + timedelta(hours=h.marcacion_3)).strftime("%H:%M")
                m4 = (datetime.min + timedelta(hours=h.marcacion_4)).strftime("%H:%M")
                horario = f"{m1} - {m2} || {m3} - {m4} => {h.dias.mapped('name')}\n"
                rec.horario_ = rec.horario_ + horario

    @api.constrains('total_horas')
    def check_total_horas(self):
        for rec in self:
            if rec.total_horas < 40 or rec.total_horas > 40:
                raise ValidationError('Favor de revisar el total de horas')

    @api.onchange('horario')
    def onchange_horario(self):
        res = 0
        for horario in self.horario:
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

    def copy(self, default=None):
        horarios = []
        for h in self.horario:
            horarios.append((0, 0, {
                'marcacion_1': h.marcacion_1,
                'marcacion_2': h.marcacion_2,
                'marcacion_3': h.marcacion_3,
                'marcacion_4': h.marcacion_4,
                'dias': h.dias
            }))
        default = {
            'horario': horarios
        }
        return super(AsignacionHorario, self).copy(default)

    @api.constrains('fecha_inicio')
    def check_horario(self):
        if not len(self) > 1:
            horarios = self.env['racetime.asignacion_horario'].search(
                [('id', '!=', self.id), ('empleado_id', '=', self.empleado_id.id),
                 ('fecha_fin', '>=', self.fecha_inicio)])
            for record in horarios:
                if record.fecha_inicio <= self.fecha_inicio and record.fecha_fin >= self.fecha_inicio:
                    raise ValidationError(
                        f"Existe un conflicto con el horario:\n"
                        f"{self.empleado_id.name}\n\n"
                        f"FECHA INICIO: {record.fecha_inicio}\n"
                        f"FECHA FIN: {record.fecha_fin}\n\n"
                        f"HORARIO: {html2plaintext(record.horario_)}")


class AsignacionHorarioMultiple(models.TransientModel):
    _name = 'racetime.asignacion_horario_multiple'
    _description = 'AsignacionHorarioMultiple'
    _inherit = 'racetime.asignacion_horario'

    empleados_ids = fields.Many2many(comodel_name='hr.employee', string='Empleados', tracking=True)
    horario_multiple = fields.Many2one(comodel_name='racetime.horarios', string='Horario', required=False)
    horario_multiple_ = fields.Html(string='Horario', required=False, store=False)
    total_horas = fields.Float(string='Total Horas', required=False, related='horario_multiple.total_horas')

    @api.constrains('total_horas')
    def check_total_horas(self):
        for rec in self.horario_multiple:
            if rec.total_horas < 40 or rec.total_horas > 40:
                raise ValidationError('Favor de revisar el total de horas')

    @api.onchange('horario_multiple')
    def _set_name_horario_multiple(self):
        self.horario_multiple_ = ""
        for horarios in self.horario_multiple.detalle_horario_id:
            for h in horarios:
                m1 = (datetime.min + timedelta(hours=h.marcacion_1)).strftime("%H:%M")
                m2 = (datetime.min + timedelta(hours=h.marcacion_2)).strftime("%H:%M")
                m3 = (datetime.min + timedelta(hours=h.marcacion_3)).strftime("%H:%M")
                m4 = (datetime.min + timedelta(hours=h.marcacion_4)).strftime("%H:%M")
                horario = f"{m1} - {m2} || {m3} - {m4} => {h.dias.mapped('name')}"
                print(horario)
                self.horario_multiple_ = self.horario_multiple_ + horario

    def generar_horarios(self):
        values = []
        for empleado in self.empleados_ids:
            horarios = []
            for h in self.horario_multiple.detalle_horario_id:
                horarios.append((0, 0, {
                    'marcacion_1': h.marcacion_1,
                    'marcacion_2': h.marcacion_2,
                    'marcacion_3': h.marcacion_3,
                    'marcacion_4': h.marcacion_4,
                    'dias': h.dias,
                }))
            values.append({
                'empleado_id': empleado.id,
                'fecha_inicio': self.fecha_inicio.strftime("%Y-%m-%d"),
                'fecha_fin': self.fecha_fin.strftime("%Y-%m-%d") if self.fecha_fin else False,
                'horario': horarios,
                'total_horas': self.total_horas
            })

        self.env['racetime.asignacion_horario'].create(values)

        return {
            'type': 'tree',
            'name': 'Asignación de Horarios',
            'context': {'search_default_group_empleado': 1},
            'view_mode': 'tree,form',
            'res_model': 'racetime.asignacion_horario',
            'type': 'ir.actions.act_window',
            'target': 'main'
        }
