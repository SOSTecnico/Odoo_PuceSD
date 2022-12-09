# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoActivo(models.Model):
    _name = 'transferencias.tipos_activos'
    _description = 'Tipo de Activo'

    name = fields.Char(string='Descripción', required=True)


class Marca(models.Model):
    _name = 'transferencias.marcas'
    _description = 'Marca'

    name = fields.Char(string="Nombre", required=True)


class Ubicacion(models.Model):
    _name = 'transferencias.ubicaciones'
    _description = 'Ubicación'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', tracking=True, track_visibility='onchange', required=True)
    departamento_id = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Departamento', required=False,
                                      tracking=True, track_visibility='onchange')


class Activo(models.Model):
    _name = 'transferencias.activos'
    _description = 'Activo Fijo'
    _rec_name = 'codigo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(string='Activo', default=True, required=False)
    codigo = fields.Char(string='Código', required=True, tracking=True, track_visibility='onchange')
    referencia = fields.Char(string='Referencia', required=False, tracking=True, track_visibility='onchange')
    responsable_id = fields.Many2one(comodel_name='hr.employee', string='Responsable', required=True, tracking=True,
                                     track_visibility='onchange')
    tipo_activo_id = fields.Many2one(comodel_name='transferencias.tipos_activos', string='Tipo de Activo',
                                     required=True, tracking=True, track_visibility='onchange')

    estado = fields.Selection(string='Estado',
                              selection=[('bueno', 'Bueno'), ('regular', 'Regular'), ('nuevo', 'Nuevo'),
                                         ('dañado', 'Dañado')],
                              required=True, tracking=True, track_visibility='onchange')

    descripcion_estado = fields.Text(string="Descripción Estado", required=False, tracking=True,
                                     track_visibility='onchange')
    ubicacion_id = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Ubicación Actual', required=False,
                                   tracking=True, track_visibility='onchange')

    serie = fields.Char(string='Serie', required=False)
