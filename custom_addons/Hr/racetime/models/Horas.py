from datetime import datetime

from odoo import fields, models, api


class Horas(models.Model):
    _name = 'racetime.horas'
    _description = 'Horas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'empleado_id'

    name = fields.Char(related='empleado_id.name')
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=True, tracking=True)
    fecha_desde = fields.Date(string='Fecha Inicio', required=False, tracking=True)
    fecha_hasta = fields.Date(string='Fecha Hasta', required=False, tracking=True)
    hora_desde = fields.Float(string='Hora Inicio', required=False, tracking=True)
    hora_hasta = fields.Float(string='Hora Fin', required=False, tracking=True)
    total_horas = fields.Float(string='Total Horas', required=False)
    descripcion = fields.Text(string="Descripción", required=False, tracking=True)
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('a_favor', 'A FAVOR'), ('extras', 'EXTRAS'), ('otros', 'OTROS')],
                            tracking=True)
    estado = fields.Selection(string='Estado', selection=[('pendiente', 'PENDIENTE'), ('aprobado', 'APROBADO'), ],
                              required=False, default='aprobado')

    aprobado_por_id = fields.Many2many(comodel_name='hr.employee', string='Aprobado por', required=False, tracking=True)
    active = fields.Boolean(string='Active', required=False, default=True, tracking=True)

    @api.onchange('fecha_desde')
    def onchange_fecha_desde(self):
        if self.fecha_desde:
            self.fecha_hasta = self.fecha_desde

    @api.model
    def create(self, values):
        # Add code here
        res = super(Horas, self).create(values)
        self.calcular_saldos(res)
        return res

    def calcular_saldos(self, values=None):
        hora = self if self else values

        horas = hora.hora_hasta - hora.hora_desde
        if hora.tipo == 'otros':
            horas = hora.total_horas

        saldo = self.env['racetime.saldos'].search([('empleado_id', '=', hora.empleado_id.id)])

        detalle_saldo = self.env['racetime.detalle_saldos'].search([('horas_id', '=', hora.id)])
        if hora.tipo == 'a_favor' or hora.tipo == 'otros':
            if not detalle_saldo:
                saldo.write({
                    'detalle_saldos': [(0, 0, {
                        'horas': horas,
                        'horas_id': hora.id,
                        'name': 'HORAS INGRESADAS',
                        'tipo': 'H',
                        'fecha': hora.fecha_desde or datetime.now()
                    })]
                })
            else:
                detalle_saldo.update({
                    'horas': horas,
                    'fecha': hora.fecha_desde or datetime.now()
                })
        else:
            detalle_saldo = self.env['racetime.detalle_saldos'].search([('horas_id', '=', hora.id)])
            saldo.write({
                'detalle_saldos': [(2, detalle_saldo.id)]
            })

    def write(self, values):
        # Add code here
        res = super(Horas, self).write(values)
        self.calcular_saldos()
        return res
