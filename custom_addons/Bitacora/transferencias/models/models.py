# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoActivo(models.Model):
    _name = 'transferencias.tipos_activos'
    _description = 'Tipo de Activo'

    name = fields.Char(string='Descripción', required=True)

    @api.onchange('name')
    def uppercase(self):
        if self.name:
            self.name = self.name.upper()


class Marca(models.Model):
    _name = 'transferencias.marcas'
    _description = 'Marca'

    name = fields.Char(string="Nombre", required=True)

    @api.onchange('name')
    def uppercase(self):
        if self.name:
            self.name = self.name.upper()


class Ubicacion(models.Model):
    _name = 'transferencias.ubicaciones'
    _description = 'Ubicación'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('ubicacion_name', 'unique(name)', 'Ya existe una ubicación con ese nombre')]

    name = fields.Char(string='Nombre', tracking=True, required=True)
    departamento_id = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Departamento', required=False,
                                      tracking=True)

    @api.onchange('name')
    def uppercase(self):
        if self.name:
            self.name = self.name.upper()


class Activo(models.Model):
    _name = 'transferencias.activos'
    _description = 'Activo Fijo'
    _rec_name = 'codigo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('codigo_activo', 'unique(codigo)', 'Ya existe un activo con el código que intenta ingresar')]

    active = fields.Boolean(string='Activo', default=True, required=False)
    codigo = fields.Char(string='Código', required=True, tracking=True)
    referencia = fields.Char(string='Referencia', required=False, tracking=True)
    responsable_id = fields.Many2one(comodel_name='hr.employee', string='Responsable', required=True, tracking=True)
    tipo_activo_id = fields.Many2one(comodel_name='transferencias.tipos_activos', string='Tipo de Activo',
                                     required=True, tracking=True)

    estado = fields.Selection(string='Estado',
                              selection=[('bueno', 'Bueno'), ('regular', 'Regular'), ('nuevo', 'Nuevo'),
                                         ('dañado', 'Dañado')],
                              required=True, tracking=True)

    descripcion_estado = fields.Text(string="Descripción Estado", required=False, tracking=True,
                                     )
    ubicacion_id = fields.Many2one(comodel_name='transferencias.ubicaciones', string='Ubicación Actual', required=False,
                                   tracking=True)

    serie = fields.Char(string='Serie', required=False)
    marca_id = fields.Many2one(comodel_name='transferencias.marcas', string='Marca', required=False)
