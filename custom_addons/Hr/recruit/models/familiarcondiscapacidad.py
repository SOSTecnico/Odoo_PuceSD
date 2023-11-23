from odoo import fields, models, api


class Familiarcondiscapacidad(models.Model):
    _name = 'recruit.familiarcondiscapacidad'
    _description = 'Description'
    _inherit = 'recruit.persona'

    parentesco = fields.Char(
        string='Parentesco',
        required=False)

    name = fields.Char(compute='_compute_name', store=True, string="Nombre Completo")

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for postulante in self:
            postulante.name = f"{postulante.nombres} {postulante.apellidos}"