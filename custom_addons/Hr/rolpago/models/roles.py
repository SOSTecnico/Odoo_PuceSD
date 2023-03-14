from datetime import datetime, timedelta

from odoo import fields, models, api
import requests
from .empleado import Empleado
import json


class Roles(models.Model):
    _name = 'rolpago.roles'
    _description = 'Roles'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin', 'utm.mixin']
    _order = 'fecha desc'

    name = fields.Char(compute='compute_name')

    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado',
        required=False)

    periodo = fields.Char(string='Periodo', required=False, compute='generar_periodo')

    rubros_id = fields.One2many(
        comodel_name='rolpago.rubros',
        inverse_name='roles_id',
        string='Rubros_id',
        required=False)

    fecha = fields.Date(string='Fecha', required=False)

    subtotal_imponibles = fields.Float(
        string='Subtotal_imponibles',
        required=False, compute='calcular_totales')

    subtotal_no_imponibles = fields.Float(
        string='Subtotal_imponibles',
        required=False, compute='calcular_totales')

    total_ingresos = fields.Float(
        string='Total_ingresos',
        required=False, compute='calcular_totales')

    total_egresos = fields.Float(
        string='Total_descuentos',
        required=False, compute='calcular_totales')

    estado_rol = fields.Selection(string='Estado', default='publicado',
                                  selection=[('publicado', 'PUBLICADO'), ('conforme', 'CONFORME'),
                                             ('no_conforme', 'NO CONFORME'), ],
                                  required=False, tracking=True)

    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s - %s' % (self.empleado_id.name, self.periodo)

    def cambiar_estado_rol(self):
        for rec in self:
            if rec.estado_rol == 'publicado' and (datetime.now() - rec.fecha) > timedelta(days=15):
                rec.estado_rol = 'conforme'

    @api.onchange('estado_rol')
    def onchange_estado(self):
        print(self.fecha)

    def calcular_totales(self):
        for rec in self:
            for rubro in rec.rubros_id:
                if rubro.tipo_rubro_id.tipo == 'I' and rubro.tipo_rubro_id.imponible == 'S':
                    rec.subtotal_imponibles = rec.subtotal_imponibles + rubro.valor
                if rubro.tipo_rubro_id.tipo == 'I' and rubro.tipo_rubro_id.imponible == 'N':
                    rec.subtotal_no_imponibles = rec.subtotal_no_imponibles + rubro.valor
                if rubro.tipo_rubro_id.tipo == 'D':
                    rec.total_egresos = rec.total_egresos + rubro.valor
            rec.total_ingresos = rec.total_ingresos + rec.subtotal_imponibles + rec.subtotal_no_imponibles

    def compute_name(self):
        for rec in self:
            rec.name = rec.periodo

    @api.model
    def generar_periodo(self):
        for rec in self:
            rec.periodo = rec.fecha.strftime("%m-%Y")

    @api.model
    def conformidad(self):
        roles = self.env['rolpago.roles'].search([])
        for rec in roles:
            if rec.estado_rol == 'publicado' and (datetime.now() - rec.create_date) > timedelta(days=15):
                rec.estado_rol = 'conforme'
