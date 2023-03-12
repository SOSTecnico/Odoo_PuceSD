from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime,timedelta

class TipoPermiso(models.Model):
    _name = 'racetime.tipos_permiso'
    _description = 'Tipo Permiso'

    name = fields.Char(string="Descripción", required=True)


class Permisos(models.Model):
    _name = 'racetime.permisos'
    _description = 'Permiso'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nombre", compute='_permiso')
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=True, tracking=True)
    aprobado_por_id = fields.Many2many(comodel_name='hr.employee', string='Aprobado Por', tracking=True)
    desde_fecha = fields.Date(string='Desde', required=False, tracking=True)
    hasta_fecha = fields.Date(string='Hasta', required=False, tracking=True)
    desde_hora = fields.Float(string='Hora Inicio', required=False, tracking=True)
    hasta_hora = fields.Float(string='Hora Fin', required=False, tracking=True)
    tipo_permiso_id = fields.Many2one(comodel_name='racetime.tipos_permiso', string='Tipo Permiso', required=True)
    descripcion = fields.Text(string="Descripción del Permiso", required=False, tracking=True)
    adjunto = fields.Binary(string="Documento")
    active = fields.Boolean(string='Active', required=False, tracking=True, default=True)
    todo_el_dia = fields.Boolean(string='Todo el Día', required=False, tracking=True)
    estado = fields.Selection(string='Estado', default='aprobado', required=True, tracking=True,
                              selection=[('pendiente', 'PENDIENTE'),
                                         ('aprobado', 'APROBADO'), ])

    @api.constrains('desde_fecha', 'hasta_fecha')
    def verificar_fechas_permiso(self):
        for rec in self:
            if rec.desde_fecha > rec.hasta_fecha:
                raise ValidationError("La fecha 'Hasta' no debe ser inferior a la fecha 'Desde'")

    @api.onchange('desde_fecha')
    def onchange_fecha(self):
        if self.desde_fecha:
            self.hasta_fecha = self.desde_fecha

    @api.depends('desde_fecha', 'hasta_fecha', 'desde_hora', 'hasta_hora', 'tipo_permiso_id')
    def _permiso(self):
        for rec in self:
            h_1 = (datetime.min + timedelta(hours=rec.desde_hora)).strftime("%H:%M")
            h_2 = (datetime.min + timedelta(hours=rec.hasta_hora)).strftime("%H:%M")
            if rec.todo_el_dia:
                rec.name = f"Desde: {rec.desde_fecha} || Hasta {rec.hasta_fecha} TIPO: {rec.tipo_permiso_id.name}"
            else:
                rec.name = f"Desde: {h_1} || Hasta {h_2} TIPO: {rec.tipo_permiso_id.name}"
