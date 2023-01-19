from datetime import datetime

from odoo import fields, models, api


class Prestamos(models.Model):
    _name = 'transferencias.prestamos'
    _description = 'Préstamo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    fecha = fields.Datetime(string='Fecha', required=True, tracking=True)
    fecha_devolucion = fields.Datetime(string='Fecha Devolución', required=False, tracking=True)
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Custodio', required=True, tracking=True)
    correo_empleado = fields.Char(string='Correo', required=False, related='empleado_id.work_email')
    unidad = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Unidad/Escuela', required=True,
                             tracking=True)
    active = fields.Boolean(string='Active', required=False, default=True, tracking=True)
    estado = fields.Selection(string='Estado', required=False, default='pendiente',
                              selection=[('pendiente', 'PENDIENTE'),
                                         ('completado', 'COMPLETADO'), ], tracking=True)
    activos_ids = fields.Many2many(comodel_name='transferencias.activos', string='Activos')
    observaciones = fields.Text(string="Observaciones", required=False, tracking=True)

    @api.onchange('fecha')
    def onchange_fecha(self):
        self.fecha = datetime.now()

    def cambiar_a_completado(self):
        self.estado = 'completado'
