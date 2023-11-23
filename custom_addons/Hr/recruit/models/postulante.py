from odoo import fields, models, api


class Postulante(models.Model):
    _name = 'recruit.postulantes'
    _description = 'Description'

    _inherit = "recruit.persona"

    name = fields.Char(compute='_compute_name', store=True, string="Nombre Completo")

    titulosycertificados_id = fields.Many2many(
        comodel_name='recruit.titulosycertificados',
        string='Titulos y certificados')

    discapacidad_id = fields.Many2many(
        comodel_name='recruit.discapacidad',
        string='Discapacidad')

    evidencias_id = fields.Many2many(
        comodel_name='recruit.evidencias',
        string='Evidencias')

    familiarcondiscapacidad_id = fields.Many2many(
        comodel_name='recruit.familiarcondiscapacidad',
        string='Familiares con discapacidad')

    contactoemergencia_id = fields.Many2many(
        comodel_name='recruit.contactoemergencia',
        string='Contacto de emergencia')

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for postulante in self:
            postulante.name = f"{postulante.nombres} {postulante.apellidos}"