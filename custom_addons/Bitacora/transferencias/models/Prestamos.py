from datetime import datetime
import random

from odoo import fields, models, api


class Prestamos(models.Model):
    _name = 'transferencias.prestamos'
    _description = 'Préstamos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def generar_codigo_prestamo(self):
        codigo = f"{datetime.now().strftime('%m%d')}-{random.randint(1000, 9999)}"
        return codigo

    name = fields.Char(default=generar_codigo_prestamo, readonly=True, string="Código Préstamo")
    fecha = fields.Datetime(string='Fecha', required=True, tracking=True)
    fecha_devolucion = fields.Datetime(string='Fecha Devolución', required=False, tracking=True)
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Custodio', required=True, tracking=True)
    correo_empleado = fields.Char(string='Correo', required=False, related='empleado_id.work_email')
    unidad = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Unidad/Escuela', required=True,
                             tracking=True, domain=[('departamento_id', '=', False)])
    active = fields.Boolean(string='Active', required=False, default=True, tracking=True)
    estado = fields.Selection(string='Estado', required=False, default='pendiente',
                              selection=[('pendiente', 'PENDIENTE'),
                                         ('completado', 'COMPLETADO'), ], tracking=True)
    activos_ids = fields.Many2many(comodel_name='transferencias.activos', string='Activos')
    observaciones = fields.Text(string="Observaciones", required=False, tracking=True)

    @api.onchange('fecha')
    def onchange_fecha(self):
        if not self.fecha:
            self.fecha = datetime.now()

    def cambiar_a_completado(self):
        self.estado = 'completado'
        self.fecha_devolucion = datetime.now()
        # Notificar via Email
        template = self.env.ref('transferencias.prestamo_resuelto_email_template')
        for rec in self:
            template.send_mail(rec.id, force_send=True)

    def cambiar_a_pendiente(self):
        self.estado = 'pendiente'
        self.fecha_devolucion = False

    def notificar_prestamo(self):
        template = self.env.ref('transferencias.prestamo_email_template')
        for rec in self:
            template.send_mail(rec.id, force_send=True)