from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TipoPermiso(models.Model):
    _name = 'racetime.tipos_permiso'
    _description = 'Tipo Permiso'

    name = fields.Char(string="Descripción", required=True)


class Permisos(models.Model):
    _name = 'racetime.permisos'
    _description = 'Permiso'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'empleado_id'

    name = fields.Char(string="Nombre", related='tipo_permiso_id.name')
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
    estado = fields.Selection(string='Estado', default='pendiente', required=True, tracking=True,
                              selection=[('pendiente', 'PENDIENTE'),
                                         ('aprobado', 'APROBADO'), ], )

    @api.constrains('desde_fecha', 'hasta_fecha')
    def verificar_fechas_permiso(self):
        for rec in self:
            if rec.desde_fecha > rec.hasta_fecha:
                raise ValidationError("La fecha 'Hasta' no debe ser inferior a la fecha 'Desde'")
