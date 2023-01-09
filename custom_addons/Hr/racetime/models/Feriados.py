from odoo import fields, models, api


class Feriados(models.Model):
    _name = 'racetime.feriados'
    _description = 'Feriado'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nombre", required=True, tracking=True)
    desde = fields.Date(string='Desde', required=True, tracking=True)
    hasta = fields.Date(string='Hasta', required=False, tracking=True)

    @api.onchange('desde')
    def onchange_desde(self):
        if self.desde:
            self.hasta = self.desde
