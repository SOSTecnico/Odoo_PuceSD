import base64
from io import BytesIO

from odoo import fields, models, api
import qrcode


class Usuario(models.Model):
    _name = 'rutas.usuarios'
    _description = 'Rutas: Usuario'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre Completo', compute='_compute_name', store=True)
    nombres = fields.Char(string='Nombres', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos', required=True, tracking=True)
    cedula = fields.Char(string='Cédula', required=True, tracking=True)
    correo = fields.Char(string='Correo', required=True, tracking=True)
    active = fields.Boolean(string='Active', required=False, default=True)
    imagenQR = fields.Image(string="", readonly=True)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for usuario in self:
            usuario.name = f"{usuario.nombres} {usuario.apellidos}"

    def generarQR(self, resource=None):
        if not resource:
            resource = self
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)

        info = {
            'id': resource.id,
            'name': resource.name
        }

        qr.add_data(info)
        qr.make(fit=True)
        temp = BytesIO()
        img = qr.make_image()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        resource.write({'imagenQR': qr_image})

    @api.model
    def create(self, values):
        res = super(Usuario, self).create(values)
        self.generarQR(resource=res)
        return res
