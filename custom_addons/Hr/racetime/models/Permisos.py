from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class TipoPermiso(models.Model):
    _name = 'racetime.tipos_permiso'
    _description = 'Tipo Permiso'

    name = fields.Char(string="Descripción", required=True)


class Permisos(models.Model):
    _name = 'racetime.permisos'
    _description = 'Permiso'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nombre", compute='_permiso')
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=False, tracking=True)
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
    estado = fields.Selection(string='Estado', default='aprobado', required=True, tracking=True,
                              selection=[('pendiente', 'PENDIENTE'),
                                         ('aprobado', 'APROBADO'), ])

    # @api.constrains('desde_fecha', 'hasta_fecha', 'desde_hora', 'hasta_hora')
    # def _check_permisos_choques(self):
    #     permisos_del_empleado = self.env['racetime.permisos'].search(
    #         [('id', '!=', self.id), ('empleado_id', '=', self.empleado_id.id), ('desde_fecha', '>=', self.desde_fecha)])
    #
    #     for rec in permisos_del_empleado:
    #
    #         if isinstance(self.desde_fecha, bool):
    #             continue
    #         if self.desde_fecha >= rec.desde_fecha and self.hasta_fecha <= rec.hasta_fecha:
    #             if rec.todo_el_dia:
    #                 raise ValidationError(
    #                     f"Existe un conflicto con el permiso:\n"
    #                     f"{self.empleado_id.name}\n\n"
    #                     f"FECHA INICIO: {rec.desde_fecha}\n"
    #                     f"FECHA FIN: {rec.hasta_fecha}\n\n"
    #                     f"HORARIO: {rec.desde_hora} || {rec.hasta_hora}")
    #             if self.desde_hora >= rec.desde_hora and self.hasta_hora <= rec.hasta_hora \
    #                     or self.desde_hora <= rec.desde_hora and self.hasta_hora >= rec.desde_hora \
    #                     or self.desde_hora >= rec.desde_hora:
    #                 raise ValidationError(
    #                     f"Existe un conflicto con el permiso:\n"
    #                     f"{self.empleado_id.name}\n\n"
    #                     f"FECHA INICIO: {rec.desde_fecha}\n"
    #                     f"FECHA FIN: {rec.hasta_fecha}\n\n"
    #                     f"HORARIO: {timedelta(hours=rec.desde_hora)} || {timedelta(hours=rec.hasta_hora)}")

    @api.constrains('desde_fecha', 'hasta_fecha')
    def verificar_fechas_permiso(self):
        for rec in self:
            if isinstance(rec.desde_fecha, bool):
                continue
            if rec.desde_fecha > rec.hasta_fecha:
                raise ValidationError("La fecha 'Hasta' no debe ser inferior a la fecha 'Desde'")

    @api.onchange('desde_fecha')
    def onchange_fecha(self):
        if self.desde_fecha:
            self.hasta_fecha = self.desde_fecha

    @api.depends('desde_fecha', 'hasta_fecha', 'desde_hora', 'hasta_hora', 'tipo_permiso_id')
    def _permiso(self):
        for rec in self:
            h_1 = (datetime.min + timedelta(hours=rec.desde_hora)).strftime("%H:%M")
            h_2 = (datetime.min + timedelta(hours=rec.hasta_hora)).strftime("%H:%M")
            if rec.todo_el_dia:
                rec.name = f"Desde: {rec.desde_fecha} || Hasta {rec.hasta_fecha} TIPO: {rec.tipo_permiso_id.name}"
            else:
                rec.name = f"Desde: {h_1} || Hasta {h_2} TIPO: {rec.tipo_permiso_id.name}"

    def calcular_saldos(self, values=None):
        permiso = self if self else values

        if permiso.tipo_permiso_id.name == 'PERSONAL':

            if permiso.todo_el_dia:
                res = (permiso.hasta_fecha - permiso.desde_fecha) + timedelta(days=1)
                horas = res.days * 8
            else:
                horas = permiso.hasta_hora - permiso.desde_hora

            saldo = self.env['racetime.saldos'].search([('empleado_id', '=', permiso.empleado_id.id)])

            detalle_saldo = self.env['racetime.detalle_saldos'].search([('permiso_id', '=', permiso.id)])

            if not detalle_saldo:
                saldo.write({
                    'detalle_saldos': [(0, 0, {
                        'horas': -horas,
                        'permiso_id': permiso.id,
                        'name': 'PERMISO APROBADO',
                        'tipo': 'P',
                        'fecha': permiso.desde_fecha
                    })]
                })
            else:
                detalle_saldo.update({
                    'horas': -horas,
                    'fecha': permiso.desde_fecha
                })

    @api.model
    def create(self, values):
        # Add code here
        res = super(Permisos, self).create(values)
        self.calcular_saldos(res)
        return res

    def write(self, values):
        # Add code here
        res = super(Permisos, self).write(values)
        self.calcular_saldos()
        return res

    def copy(self, default=None):
        default = {
            'desde_fecha': False,
            'empleado_id': False
        }
        return super(Permisos, self).copy(default)


class PermisosReportWizard(models.TransientModel):
    _name = 'racetime.permisos_report_wizard'
    _description = 'PermisosReportWizard'

    name = fields.Char()
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_fin = fields.Date(string='Fecha_fin', required=True)
    empleados = fields.Many2many(comodel_name='hr.employee', string='Empleados')


class PermisosReport(models.AbstractModel):
    _name = 'report.racetime.permisos'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'PermisosReport'

    def compute_saldo_en_dias(self, empleado, saldo_total):
        # Este código pertener al empleado ILDA ELIZALDE ella solo debe hacerce el cálculo por 6 horas
        if empleado.identification_id == '1713007910':
            dias = abs(int(saldo_total / 6))
            horas = int(abs(saldo_total) - (dias * 6))
            minutos = int(((abs(saldo_total) - (dias * 6)) - horas) * 60)
            tiempo = abs(timedelta(days=dias, hours=horas, minutes=minutos))

            saldo_en_dias = f"-{tiempo}" if saldo_total < 0 else tiempo
            return saldo_en_dias

        dias = abs(int(saldo_total / 8))
        horas = int(abs(saldo_total) - (dias * 8))
        minutos = int(((abs(saldo_total) - (dias * 8)) - horas) * 60)
        tiempo = abs(timedelta(days=dias, hours=horas, minutes=minutos))

        saldo_en_dias = f"-{tiempo}" if saldo_total < 0 else tiempo
        return saldo_en_dias

    def generate_xlsx_report(self, workbook, data, models):

        sheet_names = self.env['racetime.tipos_permiso'].search([]).mapped("name")
        sheets = {}
        sheets.update({
            'GENERAL': workbook.add_worksheet("GENERAL")
        })
        for sheet in sheet_names:
            sheets.update({
                sheet: workbook.add_worksheet(sheet)
            })

        bold = workbook.add_format({'bold': True})

        desde = models.sorted(lambda p: p.desde_fecha).mapped("desde_fecha")
        hasta = models.sorted(lambda p: p.hasta_fecha).mapped("hasta_fecha")

        sheets["GENERAL"].write("A1", "Reporte General De Permisos", bold)
        sheets["GENERAL"].write("A3", f"Desde: {desde[0]} || Hasta: {hasta[-1]} ", bold)
        sheets["GENERAL"].write("A5", "EMPLEADO", bold)
        sheets["GENERAL"].write("B5", "FECHA INICIO", bold)
        sheets["GENERAL"].write("C5", "FECHA FIN", bold)
        sheets["GENERAL"].write("D5", "HORA INICIO", bold)
        sheets["GENERAL"].write("E5", "HORA FIN", bold)
        sheets["GENERAL"].write("F5", "TOTAL HORAS", bold)
        sheets["GENERAL"].write("G5", "TIPO", bold)
        sheets["GENERAL"].write("H5", "DESCRIPCIÓN", bold)

        empleados = models.mapped("empleado_id.name")
        empleados.sort()
        fila_empleado = 5
        for empleado in empleados:
            emp = models.filtered(lambda e: e.empleado_id.name == empleado)
            try:
                permisos_del_empleado = models.filtered(lambda e: e.empleado_id.name == empleado).sorted(
                    lambda s: s.desde_fecha)

                if len(permisos_del_empleado) > 1:
                    sheets['GENERAL'].merge_range(
                        f"A{fila_empleado + 1}:A{len(permisos_del_empleado) + fila_empleado + 1}",
                        empleado)
                    total_horas = 0
                    for index, value_permiso in enumerate(permisos_del_empleado):
                        try:
                            sheets['GENERAL'].write(f"B{fila_empleado + index + 1}",
                                                    value_permiso.desde_fecha.strftime("%d-%m-%Y"))
                            sheets['GENERAL'].write(f"C{fila_empleado + index + 1}",
                                                    value_permiso.hasta_fecha.strftime("%d-%m-%Y"))

                            hora_inicio = timedelta(hours=value_permiso.desde_hora) + datetime.min
                            hora_fin = timedelta(hours=value_permiso.hasta_hora) + datetime.min

                            sheets['GENERAL'].write(f"D{fila_empleado + index + 1}",
                                                    f"{hora_inicio.strftime('%H:%M')}")

                            sheets['GENERAL'].write(f"E{fila_empleado + index + 1}",
                                                    f"{hora_fin.strftime('%H:%M')}")

                            if value_permiso.todo_el_dia:
                                dias = value_permiso.hasta_fecha - value_permiso.desde_fecha

                                if emp.empleado_id.identification_id == '1713007910':
                                    horas = (dias.days + 1) * 6
                                else:
                                    horas = (dias.days + 1) * 8

                                total_horas = horas + total_horas
                                horas = (timedelta(hours=horas) + datetime.min).strftime("%H:%M")


                            else:
                                total_horas = (value_permiso.hasta_hora - value_permiso.desde_hora) + total_horas
                                horas = ((hora_fin - hora_inicio) + datetime.min).strftime("%H:%M")

                            sheets['GENERAL'].write(f"F{fila_empleado + index + 1}",
                                                    f"{horas}")

                            sheets['GENERAL'].write(f"G{fila_empleado + index + 1}",
                                                    f"{value_permiso.tipo_permiso_id.name}")
                            sheets['GENERAL'].write(f"H{fila_empleado + index + 1}",
                                                    f"{value_permiso.descripcion or ''}")

                        except Exception as e:
                            print(e)
                            continue
                    sheets['GENERAL'].write(f"E{fila_empleado + len(permisos_del_empleado) + 1}",
                                            "Total", bold)
                    sheets['GENERAL'].write(f"F{fila_empleado + len(permisos_del_empleado) + 1}",
                                            f"{round(total_horas, 2)}", bold)
                    fila_empleado = len(permisos_del_empleado) + fila_empleado + 1

                else:
                    sheets['GENERAL'].merge_range(f"A{fila_empleado + 1}:A{fila_empleado + 2}", empleado)

                    sheets['GENERAL'].write(f"B{fila_empleado + 1}",
                                            permisos_del_empleado.desde_fecha.strftime("%d-%m-%Y"))
                    sheets['GENERAL'].write(f"C{fila_empleado + 1}",
                                            permisos_del_empleado.hasta_fecha.strftime("%d-%m-%Y"))

                    hora_inicio = timedelta(hours=permisos_del_empleado.desde_hora) + datetime.min
                    hora_fin = timedelta(hours=permisos_del_empleado.hasta_hora) + datetime.min

                    sheets['GENERAL'].write(f"D{fila_empleado + 1}",
                                            f"{hora_inicio.strftime('%H:%M')}")

                    sheets['GENERAL'].write(f"E{fila_empleado + 1}",
                                            f"{hora_fin.strftime('%H:%M')}")
                    sheets['GENERAL'].write(f"E{fila_empleado + 2}",
                                            "Total", bold)
                    total_horas = 0
                    if permisos_del_empleado.todo_el_dia:

                        dias = permisos_del_empleado.hasta_fecha - permisos_del_empleado.desde_fecha

                        if emp.empleado_id.identification_id == '1713007910':
                            horas = (dias.days + 1) * 6
                        else:
                            horas = (dias.days + 1) * 8
                        total_horas = horas
                    else:
                        horas = ((hora_fin - hora_inicio) + datetime.min).strftime("%H:%M")
                        total_horas = round((hora_fin - hora_inicio).total_seconds() / 3600,2)

                    sheets['GENERAL'].write(f"F{fila_empleado + 1}",
                                            f"{horas}")
                    sheets['GENERAL'].write(f"F{fila_empleado + 2}",
                                            f"{total_horas}", bold)
                    sheets['GENERAL'].write(f"G{fila_empleado + 1}",
                                            f"{permisos_del_empleado.tipo_permiso_id.name}")
                    sheets['GENERAL'].write(f"H{fila_empleado + 1}",
                                            f"{permisos_del_empleado.descripcion or ''}")

                    fila_empleado = fila_empleado + 2
            except Exception as e:
                print(empleado)
                print(e)
                continue
