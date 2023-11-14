from odoo import models, fields


class TipoHistorial(models.Model):
    _name = 'banner.historial_notificacion'
    _description = 'Historial de Notificaciones'

    fecha = fields.Datetime(String='Fecha')
    usuario = fields.Many2one(String='Usuario', comodel_name="banner.usuarios")
    #Asunto = fields.Many2one(String='Asunto')

    # tree formulario accion menuitem vistas
