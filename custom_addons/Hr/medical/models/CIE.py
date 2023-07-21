from odoo import fields, models, api


class Cie10(models.Model):
    _name = 'medical.cie10'
    _description = 'Código CIE 10'

    name = fields.Char(string='Código CIE 10')

    codigo = fields.Char(string='Código', required=True)
    descripcion = fields.Char(string='Descripción', required=True)

    def name_get(self):
        result = []

        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.codigo, rec.descripcion)))

        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=2, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('codigo', operator, name), ('descripcion', operator, name)]
        return self._search(domain + args, limit=limit)
