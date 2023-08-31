# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api, modules
import qrcode
from PIL import Image
from io import BytesIO


class Visitas(models.Model):
    _name = 'visitas.visitas'
    _description = 'Visita'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(string='Active', required=False, default=True)
    name = fields.Char(string='Name', required=False, related='visitante_id.name')

    fecha_inicio = fields.Date(string='Fecha', required=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=False)
    visitante_id = fields.Many2one(comodel_name='visitas.visitantes', string='Visitante', required=False)
    receptor_id = fields.Many2one(comodel_name='hr.employee', string='Receptor', required=True)
    departamento_id = fields.Many2one(comodel_name='hr.department', string='Departamento')
    motivo = fields.Text(string="Motivo", required=True)
    qr = fields.Image(string="Código QR", readonly=True)

    @api.onchange('receptor_id')
    def onchange_receptor(self):
        if self.receptor_id:
            self.departamento_id = self.receptor_id.department_id

    def generarQR(self):
        image_path = modules.module.get_resource_path("visitas", "static/assets", "logoPUCESD.jpeg")
        logo = Image.open(image_path)

        # taking base width
        basewidth = 200

        # adjust image size
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

        secret = b'{self.create_date.strftime("%Y-%m-%d")}'

        info = {
            'fecha_inicio': self.fecha_inicio.strftime("%Y-%m-%d"),
            'fecha_fin': self.fecha_fin.strftime("%Y-%m-%d"),
            'receptor': self.receptor_id.name,
            'visitante': {
                'nombre': self.visitante_id.name,
                'cedula': self.visitante_id.cedula,
                'correo': self.visitante_id.correo,
            },
            'departamento': self.departamento_id.name,
            'motivo': self.motivo,
            'x_x': base64.b64encode(secret).decode('ascii')
        }

        # adding URL or text to QRcode
        QRcode.add_data(info)

        # generating QR code
        QRcode.make(fit=True)

        # adding color to QR code
        QRimg = QRcode.make_image().convert('RGB')

        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

        temp = BytesIO()

        # save the QR code generated
        QRimg.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr = qr_image

    def enviarQR(self):
        pass

    @api.model
    def create(self, values):
        # Add code here
        res = super(Visitas, self).create(values)

        res.generarQR()

        return res
