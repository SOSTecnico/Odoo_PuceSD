# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TipoTransferencia(models.Model):
    _name = 'transferencias.tipos_transferencias'
    _description = 'Tipo Transferencia'

    name = fields.Char(string="Tipo de Transferencia", required=True)

    @api.onchange('name')
    def uppercase(self):
        if self.name:
            self.name = self.name.upper()


class Transferencia(models.Model):
    _name = 'transferencias.transferencias'
    _description = 'Transferencia'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'codigo'
    _sql_constraints = [
        ('codigo_transferencia', 'unique(codigo)', 'Ya existe una Transferencia con el código que intenta ingresar')]

    fecha = fields.Date(string='Fecha', required=True, default=lambda self: datetime.now(), tracking=True)
    codigo = fields.Char(string='Código', required=True, tracking=True)
    tipo_transferencia_id = fields.Many2one(comodel_name='transferencias.tipos_transferencias',
                                            string='Tipo de Transferencia', required=True)
    custodio_origen_id = fields.Many2one(comodel_name='hr.employee', string='Custodio Origen', required=True,
                                         tracking=True)

    custodio_destino_id = fields.Many2one(comodel_name='hr.employee', string='Custodio Destino', required=True,
                                          tracking=True)

    ubicacion_origen_id = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Ubicación Origen',
                                          required=True, tracking=True)

    ubicacion_destino_id = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Ubicación Destino',
                                           required=True, tracking=True)

    activos_ids = fields.Many2many(comodel_name='transferencias.activos', string='Activos', required=True)
    observaciones = fields.Text(string="Observaciones", required=False)

    archivo = fields.Binary(string="Evidencia Digital")
    nombre_archivo = fields.Char(string='Evidencia Digital', required=False)

    clausula = """Como funcionario de la Pontificia Universidad Católica del Ecuador Sede Santo Domingo acepto que los activos relacionados en el presente documento están  bajo  mi  responsabilidad,  por  lo  cual  les  daré un uso adecuado al  desempeño de mis funciones y a la destinación institucional prevista para cada uno de ellos. En consecuencia, serán asumidos por mí el daño o la pérdida de los mismos debidos a mi negligencia o incumplimiento de los instructivos relacionados con su uso y conservación. Me comprometo  a  informar  oportunamente  a  la Oficina de Activos Fijos sobre cualquier desplazamiento, traslado temporal o definitivo de dichos activos mediante la tramitación de los formatos respectivos, y sobre cualquier situación que ponga en inminente riesgo los bienes relacionados."""

    @api.constrains('archivo', 'nombre_archivo')
    def _check_file_type(self):

        if self.nombre_archivo and not self.nombre_archivo.endswith('.pdf'):
            raise ValidationError('Solo se permite la Evidencia en formato PDF')

    @api.model
    def create(self, values):

        res = super(Transferencia, self).create(values)
        for activo in res.activos_ids:
            activo.responsable_id = res.custodio_destino_id
            activo.ubicacion_id = res.ubicacion_destino_id

        return res
