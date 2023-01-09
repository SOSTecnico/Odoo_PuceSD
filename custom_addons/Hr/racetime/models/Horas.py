from odoo import fields, models, api


class Horas(models.Model):
    _name = 'racetime.horas'
    _description = 'Horas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'empleado_id'

    name = fields.Char(related='empleado_id.name')
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=True, tracking=True)
    inicio = fields.Datetime(string='Inicio', required=True, tracking=True)
    fin = fields.Datetime(string='Fin', required=True, tracking=True)
    descripcion = fields.Text(string="Descripción", required=True, tracking=True)
    tipo = fields.Selection(string='Tipo', required=True, selection=[('a_favor', 'A FAVOR'), ('extras', 'EXTRAS')],
                            tracking=True)
    estado = fields.Selection(string='Estado', selection=[('pendiente', 'PENDIENTE'), ('aprobado', 'APROBADO'), ],
                              required=False, )

    aprobado_por_id = fields.Many2many(comodel_name='hr.employee', string='Aprobado por', required=False, tracking=True)
    active = fields.Boolean(string='Active', required=False, default=True, tracking=True)
