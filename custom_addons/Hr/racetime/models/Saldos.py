from odoo import fields, models, api


class Saldos(models.Model):
    _name = 'racetime.saldos'
    _description = 'Saldos'

    name = fields.Char()
    saldo_total = fields.Float(string='Saldo Total', required=False, compute='_compute_saldo_total')
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=True)
    detalle_saldos = fields.One2many(comodel_name='racetime.detalle_saldos', inverse_name='saldo_id',
                                     string='Detalle de Saldos', required=False)

    @api.depends('detalle_saldos')
    def _compute_saldo_total(self):
        for rec in self:
            total = 0
            for saldo in rec.detalle_saldos:
                if saldo.tipo == 'P':
                    total = total - saldo.horas
                if saldo.tipo == 'H' or saldo.tipo == 'I' or saldo.tipo == 'VA' or saldo.tipo == 'BA':
                    total = total + saldo.horas

            rec.saldo_total = total

    def calcular_saldos_manual(self):

        permisos_del_empleado = self.env['racetime.permisos'].search([('empleado_id', '=', self.empleado_id.id)])
        horas_del_empleado = self.env['racetime.horas'].search(
            [('empleado_id', '=', self.empleado_id.id), ('tipo', '=', 'a_favor')])
        saldos = self.env['racetime.saldos'].search([('empleado_id', '=', self.empleado_id.id)])

        data = []
        for permiso in permisos_del_empleado:
            if permiso.tipo_permiso_id.name == 'PERSONAL':
                detalle_saldo = saldos.detalle_saldos.filtered_domain([('permiso_id', '=', permiso.id)])
                if not detalle_saldo:
                    data.append((0, 0, {
                        'horas': (permiso.hasta_hora - permiso.desde_hora) * 3600,
                        'fecha': permiso.desde_fecha,
                        'tipo': 'P',
                        'permiso_id': permiso.id,
                        'name': 'PERMISO APROBADO'
                    }))
                else:
                    data.append((1, detalle_saldo.id, {
                        'horas': (permiso.hasta_hora - permiso.desde_hora) * 3600,
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
        self.write({
            'detalle_saldos': data
        })


class DetalleSaldos(models.Model):
    _name = 'racetime.detalle_saldos'
    _description = 'DetalleSaldos'
    _order = 'fecha desc'

    name = fields.Char(string="Concepto")
    saldo_id = fields.Many2one(comodel_name='racetime.saldos', string='Saldo', required=False, ondelete='cascade')
    permiso_id = fields.Many2one(comodel_name='racetime.permisos', string='Permisos ID', required=False,
                                 ondelete='cascade')
    horas_id = fields.Many2one(comodel_name='racetime.horas', string='Horas ID', required=False, ondelete='cascade')
    fecha = fields.Date(string='Fecha', required=False)
    tipo = fields.Selection(string='Tipo', selection=[('P', 'Permiso'), ('H', 'Horas a Favor'), ('I', 'Saldo Inicial'),
                                                      ('VA', 'Vacaciones Antiguedad'), ('BA', 'Beneficios Antiguedad')],
                            required=True, )

    horas = fields.Float(string='Horas', required=False)
