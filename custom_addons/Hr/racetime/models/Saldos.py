from odoo import fields, models, api
from datetime import timedelta, datetime

from odoo.exceptions import ValidationError

import xlsxwriter


class Saldos(models.Model):
    _name = 'racetime.saldos'
    _description = 'Saldos'
    _rec_name = 'empleado_id'

    active = fields.Boolean(string='Active', required=False, default=True)
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

            # Este código pertener al empleado ILDA ELIZALDE ella solo debe hacerce el cálculo por 6 horas
            if rec.empleado_id.identification_id == '1713007910':
                dias = abs(int(rec.saldo_total / 6))
                horas = int(abs(rec.saldo_total) - (dias * 6))
                minutos = int(((abs(rec.saldo_total) - (dias * 6)) - horas) * 60)
                tiempo = abs(timedelta(days=dias, hours=horas, minutes=minutos))

                rec.saldo_en_dias = f"-{tiempo}" if rec.saldo_total < 0 else tiempo
                continue

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

                            # Este código pertener al empleado ILDA ELIZALDE ella solo debe hacerce el cálculo por 6 horas
                            if rec.empleado_id.identification_id == '1713007910':
                                total = res.days * 6

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

                            # Este código pertener al empleado ILDA ELIZALDE ella solo debe hacerce el cálculo por 6 horas
                            if rec.empleado_id.identification_id == '1713007910':
                                total = res.days * 6
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
                        'horas': hora.hora_hasta - hora.hora_desde,
                        'fecha': hora.fecha_desde,
                        'tipo': 'H',
                        'horas_id': hora.id,
                        'name': 'HORAS INGRESADAS'
                    }))
                else:
                    data.append((1, hora_emp.id, {
                        'horas': hora.hora_hasta - hora.hora_desde,
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
                                       ('DA', 'Días Antiguedad'), ('DB', 'Días Beneficio'), ('DH', 'Descuento Horas')],
                            required=True, tracking=True)

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=False,
                                  related='saldo_id.empleado_id')
    horas = fields.Float(string='Horas', required=False, tracking=True)

    @api.onchange('horas')
    def onchange_horas(self):
        if self.horas:
            if self.tipo == 'P':
                self.horas = f"-{self.horas}"


class SaldosWizard(models.TransientModel):
    _name = 'racetime.saldos_wizard'
    _description = 'SaldosWizard'

    name = fields.Char()

    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True)
    empleados = fields.Many2many(comodel_name='hr.employee', string='Empleados')

    def generar_reporte(self):
        data = {
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'empleados': self.empleados.ids
        }
        return self.env.ref('racetime.saldos_report_xlsx').report_action(self, data=data)


class SaldosReport(models.AbstractModel):
    _name = 'report.racetime.saldos'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'SaldosReport'

    def generate_xlsx_report(self, workbook, data, records):
        empleados = self.env['hr.employee'].search([('id', 'in', data['empleados'])])
        detalle_de_saldos = self.env['racetime.detalle_saldos'].search(
            [('empleado_id', 'in', data['empleados']), ('fecha', '>=', data['fecha_inicio']),
             ('fecha', '<=', data['fecha_fin'])])

        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet("Reporte de Saldos")
        sheet.write("B1", "Reporte General De Saldos", bold)
        sheet.write("B2", f"Desde: {data['fecha_inicio']} || Hasta: {data['fecha_fin']}", bold)
        sheet.write("A4", "Cédula", bold)
        sheet.write("B4", "Empleados", bold)
        # print(data)
        celda_inicio = 5
        for i, empleado in enumerate(empleados):
            sheet.write(f"A{i + celda_inicio}", empleado.identification_id)
            sheet.write(f"B{i + celda_inicio}", empleado.name)
        # sheet.write(2, 0, f"Desde: {desde[0]} || Hasta: {hasta[-1]} ", bold)
        # sheet.write(4, 0, "CÉDULA", bold)
        # sheet.write(4, 1, "EMPLEADO", bold)
        # sheet.write(4, 2, "SALDO ANTERIOR", bold)
        # sheet.write(4, 3, "VACACIONES ANTIGUEDAD", bold)
        # sheet.write(4, 4, "BENEFICIOS ANTIGUEDAD", bold)
        # sheet.write(4, 5, "HORAS ADICIONALES", bold)
        # sheet.write(4, 6, "PERMISOS", bold)
        # sheet.write(4, 7, "DESCUENTO HORAS", bold)
        # sheet.write(4, 8, "SALDO EN HORAS", bold)
        # sheet.write(4, 9, "SALDO EN DÍAS", bold)

        # raise ValidationError("posi")

        # sheet_names = self.env['racetime.tipos_permiso'].search([]).mapped("name")
        # sheets = {}
        # sheets.update({
        #     'GENERAL': workbook.add_worksheet("GENERAL")
        # })
        # for sheet in sheet_names:
        #     sheets.update({
        #         sheet: workbook.add_worksheet(sheet)
        #     })
        #
        # bold = workbook.add_format({'bold': True})
        #
        # desde = models.sorted(lambda p: p.desde_fecha).mapped("desde_fecha")
        # hasta = models.sorted(lambda p: p.hasta_fecha).mapped("hasta_fecha")
        #
        # sheets["GENERAL"].write(0, 0, "Reporte General De Permisos", bold)
        # sheets["GENERAL"].write(2, 0, f"Desde: {desde[0]} || Hasta: {hasta[-1]} ", bold)
        # sheets["GENERAL"].write(4, 0, "EMPLEADO", bold)
        # sheets["GENERAL"].write(4, 1, "FECHA", bold)
        # sheets["GENERAL"].write(4, 2, "HORAS", bold)
        #
        # empleados = models.mapped("empleado_id.name")
        # empleados.sort()
        # fila_empleado = 5
        # for empleado in empleados:
        #     permisos_del_empleado = models.filtered(lambda e: e.empleado_id.name == empleado)
        #     if len(permisos_del_empleado) > 1:
        #         sheets['GENERAL'].merge_range(f"A{fila_empleado+1}:A{len(permisos_del_empleado) + fila_empleado}",
        #                                       empleado)
        #         fila_empleado = len(permisos_del_empleado) + fila_empleado
        #     else:
        #         sheets['GENERAL'].write(fila_empleado, 0, empleado)
        #         fila_empleado = fila_empleado + 1
        #     for permiso in permisos_del_empleado:
        #         pass
