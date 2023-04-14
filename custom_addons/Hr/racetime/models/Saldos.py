from odoo import fields, models, api
from datetime import timedelta
from math import ceil, floor


class Saldos(models.Model):
    _name = 'racetime.saldos'
    _description = 'Saldos'
    _rec_name = 'empleado_id'

    name = fields.Char()
    saldo_total = fields.Float(string='Saldo Total', required=False, compute='_compute_saldo_total')
    saldo_en_dias = fields.Char(string='Saldo en Días', required=False, compute='_compute_saldo_en_dias')
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=True)
    detalle_saldos = fields.One2many(comodel_name='racetime.detalle_saldos', inverse_name='saldo_id',
                                     string='Detalle de Saldos', required=False)

    @api.depends('detalle_saldos')
    def _compute_saldo_total(self):
        for rec in self:
            total = 0
            for saldo in rec.detalle_saldos:
                total = total + saldo.horas

            rec.saldo_total = total

    @api.depends('saldo_total')
    def _compute_saldo_en_dias(self):
        for rec in self:
            dias = abs(int(rec.saldo_total / 8))
            horas = int(abs(rec.saldo_total) - (dias * 8))
            minutos = int(((abs(rec.saldo_total) - (dias * 8)) - horas) * 60)
            tiempo = abs(timedelta(days=dias, hours=horas, minutes=minutos))

            rec.saldo_en_dias = f"-{tiempo}" if rec.saldo_total < 0 else tiempo

    def calcular_saldos_manual(self):

        for rec in self:
            permisos_del_empleado = self.env['racetime.permisos'].search([('empleado_id', '=', rec.empleado_id.id)])
            horas_del_empleado = self.env['racetime.horas'].search(
                [('empleado_id', '=', rec.empleado_id.id), ('tipo', '=', 'a_favor')])
            saldos = self.env['racetime.saldos'].search([('empleado_id', '=', rec.empleado_id.id)])

            data = []
            for permiso in permisos_del_empleado:
                if permiso.tipo_permiso_id.name == 'PERSONAL':
                    detalle_saldo = saldos.detalle_saldos.filtered_domain([('permiso_id', '=', permiso.id)])
                    if not detalle_saldo:
                        if permiso.todo_el_dia:
                            res = (permiso.hasta_fecha - permiso.desde_fecha) + timedelta(days=1)
                            total = res.days * 8
                        else:
                            total = permiso.hasta_hora - permiso.desde_hora
                        data.append((0, 0, {
                            'horas': -total,
                            'fecha': permiso.desde_fecha,
                            'tipo': 'P',
                            'permiso_id': permiso.id,
                            'name': 'PERMISO APROBADO'
                        }))
                    else:
                        if permiso.todo_el_dia:
                            res = (permiso.hasta_fecha - permiso.desde_fecha) + timedelta(days=1)
                            total = res.days * 8
                        else:
                            total = permiso.hasta_hora - permiso.desde_hora
                        data.append((1, detalle_saldo.id, {
                            'horas': -total,
                            'fecha': permiso.desde_fecha,
                            'tipo': 'P',
                            'permiso_id': permiso.id,
                            'name': 'PERMISO APROBADO'
                        }))

            for hora in horas_del_empleado:
                hora_emp = saldos.detalle_saldos.filtered_domain([('horas_id', '=', hora.id)])
                if not hora_emp:
                    data.append((0, 0, {
                        'horas': (hora.hora_hasta - hora.hora_desde) * 3600,
                        'fecha': hora.fecha_desde,
                        'tipo': 'H',
                        'horas_id': hora.id,
                        'name': 'HORAS INGRESADAS'
                    }))
                else:
                    data.append((1, hora_emp.id, {
                        'horas': (hora.hora_hasta - hora.hora_desde) * 3600,
                        'fecha': hora.fecha_desde,
                        'tipo': 'H',
                        'horas_id': hora.id,
                        'name': 'HORAS INGRESADAS'
                    }))
            rec.write({
                'detalle_saldos': data
            })

    def reestablecer_saldos(self):
        for rec in self:
            detalle_saldos = rec.detalle_saldos.filtered_domain([('tipo', '!=', 'SC')])
            detalle_saldos.unlink()


class DetalleSaldos(models.Model):
    _name = 'racetime.detalle_saldos'
    _description = 'DetalleSaldos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha desc'

    name = fields.Char(string="Concepto")
    saldo_id = fields.Many2one(comodel_name='racetime.saldos', string='Saldo', required=False, ondelete='cascade',
                               tracking=True)
    permiso_id = fields.Many2one(comodel_name='racetime.permisos', string='Permisos ID', required=False,
                                 ondelete='cascade', tracking=True)
    horas_id = fields.Many2one(comodel_name='racetime.horas', string='Horas ID', required=False, ondelete='cascade',
                               tracking=True)
    fecha = fields.Date(string='Fecha', required=False, tracking=True)
    tipo = fields.Selection(string='Tipo',
                            selection=[('P', 'Permiso'), ('H', 'Horas a Favor'), ('SC', 'Saldo al Corte'),
                                       ('DA', 'Días Antiguedad'), ('DB', 'Días Beneficio')],
                            required=True, tracking=True)

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=False,
                                  related='saldo_id.empleado_id')
    horas = fields.Float(string='Horas', required=False, tracking=True)

    @api.onchange('horas')
    def onchange_horas(self):
        if self.horas:
            if self.tipo == 'P':
                self.horas = f"-{self.horas}"
