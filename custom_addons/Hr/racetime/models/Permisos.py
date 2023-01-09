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
    desde = fields.Datetime(string='Desde', required=True, tracking=True)
    hasta = fields.Datetime(string='Hasta', required=True, tracking=True)
    tipo_permiso_id = fields.Many2one(comodel_name='racetime.tipos_permiso', string='Tipo Permiso', required=True)
    descripcion = fields.Text(string="Descripción del Permiso", required=True, tracking=True)
    adjunto = fields.Binary(string="Documento")
    active = fields.Boolean(string='Active', required=False, tracking=True, default=True)
    estado = fields.Selection(string='Estado', default='pendiente', required=True, tracking=True,
                              selection=[('pendiente', 'PENDIENTE'),
                                         ('aprobado', 'APROBADO'), ], )

    @api.constrains('desde', 'hasta')
    def verificar_fechas_permiso(self):
        for rec in self:
            if rec.desde > rec.hasta:
                raise ValidationError("La fecha 'Hasta' no debe ser inferior a la fecha 'Desde'")

