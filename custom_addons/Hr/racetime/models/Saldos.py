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
            detalle_saldos = rec.detalle_saldos.filtered_domain([('tipo', '=', 'SC')]).sorted(lambda r: r.fecha)
            total = 0

            if len(detalle_saldos) > 0:
                saldo_al_corte = detalle_saldos[-1]
                total = saldo_al_corte.horas
                # detalle_saldos = self.env['racetime.detalle_saldos'].search([('id', 'in', rec.detalle_saldos.ids)],
                #                                                             order='fecha asc, saldo desc')
                for saldo in rec.detalle_saldos.filtered_domain([('fecha', '>', saldo_al_corte.fecha)]):
                    total = total + saldo.horas
                    # saldo.saldo = total

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

    def generar_corte(self):
        for rec in self:
            detalle_saldos = rec.detalle_saldos.filtered_domain(
                [('fecha', '=', datetime.now().strftime("%Y-%m-%d")), ('tipo', '=', 'SC')])

            if not detalle_saldos:
                rec.detalle_saldos.create({
                    'tipo': 'SC',
                    'horas': rec.saldo_total,
                    'fecha': datetime.now(),
                    'saldo_id': rec.id
                })
            else:
                detalle_saldos.update({
                    'horas': rec.saldo_total,
                })


class DetalleSaldos(models.Model):
    _name = 'racetime.detalle_saldos'
    _description = 'DetalleSaldos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha desc, horas desc'

    name = fields.Char(string="Concepto")
    saldo_id = fields.Many2one(comodel_name='racetime.saldos', string='Saldo ID', required=False, ondelete='cascade',
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

    # saldo = fields.Float(string='Saldo', required=False)

    @api.onchange('horas', 'tipo')
    def onchange_horas(self):
        if self.horas:
            if self.tipo == 'P' or self.tipo == 'DH':
                self.horas = f"-{abs(self.horas)}"
            else:
                self.horas = abs(self.horas)


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

        fecha_inicio = self.obtener_detalle_de_saldo_al_corte(records[0], field='fecha')

        # Configuración inicial de la plantilla de Excel
        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet("Reporte de Saldos")
        sheet.write("B1", "Reporte General De Saldos", bold)
        sheet.write("B2", f"Desde: {fecha_inicio} || Hasta: {datetime.now().strftime('%Y-%m-%d')}", bold)
        sheet.write("A4", "Cédula", bold)
        sheet.write("B4", "Empleados", bold)
        sheet.write("B4", "Empleados", bold)
        sheet.write("C4", "Saldo Anterior", bold)
        sheet.write("D4", "Vacaciones Antiguedad", bold)
        sheet.write("E4", "Beneficios Antiguedad", bold)
        sheet.write("F4", "H. Adicionales", bold)
        sheet.write("G4", "Permisos", bold)
        sheet.write("H4", "Descuento Horas", bold)
        sheet.write("I4", "Saldo en Horas", bold)
        sheet.write("J4", "Saldo en Días", bold)

        nombres_empleados = records.mapped('empleado_id.name')
        empleados = self.env['hr.employee'].search([('name', 'in', nombres_empleados)])

        celda_inicio = 5
        for i, empleado in enumerate(empleados):
            try:
                sheet.write(f"A{i + celda_inicio}", empleado.identification_id)
                sheet.write(f"B{i + celda_inicio}", empleado.name)

                saldo = records.filtered_domain([('empleado_id', '=', empleado.id)])
                fecha_al_corte = self.obtener_detalle_de_saldo_al_corte(saldo=saldo, field='fecha')

                sheet.write(f"C{i + celda_inicio}", self.obtener_detalle_de_saldo_al_corte(saldo=saldo, field='horas'))

                dias_antiguedad = sum(
                    saldo.detalle_saldos.filtered_domain(
                        [('fecha', '>=', fecha_al_corte), ('tipo', '=', 'DA'), ]).mapped(
                        'horas'))
                sheet.write(f"D{i + celda_inicio}", round(dias_antiguedad, 2))

                dias_beneficio = sum(
                    saldo.detalle_saldos.filtered_domain([('fecha', '>=', fecha_al_corte), ('tipo', '=', 'DB')]).mapped(
                        'horas'))
                sheet.write(f"E{i + celda_inicio}", round(dias_beneficio, 2))

                horas_adicionales = sum(
                    saldo.detalle_saldos.filtered_domain([('fecha', '>=', fecha_al_corte), ('tipo', '=', 'H')]).mapped(
                        'horas'))
                sheet.write(f"F{i + celda_inicio}", round(horas_adicionales, 2))

                permisos = sum(
                    saldo.detalle_saldos.filtered_domain([('fecha', '>=', fecha_al_corte), ('tipo', '=', 'P')]).mapped(
                        'horas'))
                sheet.write(f"G{i + celda_inicio}", round(permisos, 2))

                descuento_horas = sum(
                    saldo.detalle_saldos.filtered_domain([('fecha', '>=', fecha_al_corte), ('tipo', '=', 'DH')]).mapped(
                        'horas'))
                sheet.write(f"H{i + celda_inicio}", round(descuento_horas, 2))

                saldo_total_en_horas = sum(
                    saldo.detalle_saldos.filtered_domain([('fecha', '>=', fecha_al_corte)]).mapped(
                        'horas'))
                sheet.write(f"I{i + celda_inicio}", round(saldo_total_en_horas, 2))
                sheet.write(f"J{i + celda_inicio}", saldo.saldo_en_dias)
            except:
                continue

    def obtener_detalle_de_saldo_al_corte(self, saldo, field):
        rec = saldo.detalle_saldos.filtered_domain([('tipo', '=', 'SC')]).sorted(lambda s: s.fecha)
        try:
            return rec[-1].read()[0][field]
        except:
            return 0
