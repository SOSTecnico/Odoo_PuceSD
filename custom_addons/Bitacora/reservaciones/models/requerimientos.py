from odoo import fields, models, api


class DetalleRequerimiento(models.Model):
    _name = 'reservaciones.detalle_req'
    _description = 'Detalle Requerimiento'

    name = fields.Char(string="Descripción")


class Requerimiento(models.Model):
    _name = 'reservaciones.req'
    _description = 'Requerimiento'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'codigo'

    codigo = fields.Char(string="Código", required=True, tracking=True)

    det_req_id = fields.Many2many(comodel_name='reservaciones.detalle_req', string='Detalle Requerimiento',
                                  required=True, tracking=True)

    recurso_id = fields.Many2one(comodel_name='reservaciones.recursos', string='Recurso', required=False, tracking=True)

    solicitante_id = fields.Many2one(comodel_name='hr.employee', string='Solicitante', required=False, tracking=True)

    observaciones = fields.Text(string="Observaciones", required=False, tracking=True)

    active = fields.Boolean(string='State', required=False, default=True, tracking=True)

    estado = fields.Selection(
        string='Estado',
        selection=[('pendiente', 'PENDIENTE'),
                   ('realizado', 'REALIZADO'), ],
        required=True, default='pendiente', tracking=True)

    def req_realizado(self):
        self.estado = 'realizado'
