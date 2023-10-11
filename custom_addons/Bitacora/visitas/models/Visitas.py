# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api, modules
import qrcode
from PIL import Image
from io import BytesIO

import logging

_logger = logging.getLogger(__name__)


class Visitas(models.Model):
    _name = 'visitas.visitas'
    _description = 'Visita'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(string='Active', required=False, default=True)
    name = fields.Char(string='Name', required=False, related='visitante_id.name')

    # fecha_inicio = fields.Date(string='Fecha', required=True)
    # fecha_fin = fields.Date(string='Fecha Fin', required=False)
    visitante_id = fields.Many2one(comodel_name='visitas.visitantes', string='Visitante', required=False)
    receptor_id = fields.Many2one(comodel_name='hr.employee', string='Receptor')
    departamento_id = fields.Many2one(comodel_name='hr.department', string='Departamento')
    motivo = fields.Text(string="Motivo", required=True)
    qr = fields.Image(string="Código QR", readonly=True)

    valido_hasta = fields.Date(string='Válido Hasta', required=False, tracking=True)
    estado = fields.Selection(string='Estado', selection=[('valido', 'Válido'), ('no_valido', 'No Válido'), ],
                              default='valido', tracking=True)

    @api.onchange('receptor_id')
    def onchange_receptor(self):
        if self.receptor_id:
            self.departamento_id = self.receptor_id.department_id

    def generarQR(self):
        image_path = modules.module.get_resource_path("visitas", "static/assets", "logo.png")
        logo = Image.open(image_path).convert("RGBA")

        basewidth = 150

        # adjust image size
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        date = self.valido_hasta.strftime("%Y-%m-%d") if self.valido_hasta else 0
        info = {
            'id': self.id,
            'valido_hasta': date,
            'estado': self.estado
        }

        data = base64.b64encode(str(info).encode('utf-8'))

        # adding URL or text to QRcode
        QRcode.add_data(data)

        # generating QR code
        QRcode.make(fit=True)

        # adding color to QR code
        QRimg = QRcode.make_image().convert('RGB')

        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos, logo)

        temp = BytesIO()

        # save the QR code generated
        QRimg.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr = qr_image

    def enviarQR(self):
        template_id = self.env.ref("visitas.codigo_qr_email_template").id
        for rec in self:
            if rec.visitante_id.correo:
                self.env["mail.template"].sudo().browse(template_id).send_mail(rec.id, force_send=True)
        _logger.info(f"{len(self)} Correo(s) Enviado(s) Correctamente!")

    def cambiar_a_valido(self):
        for r in self:
            r.estado = 'valido'

    def cambiar_a_no_valido(self):
        for r in self:
            r.estado = 'no_valido'

    @api.model
    def create(self, values):
        # Add code here
        res = super(Visitas, self).create(values)

        res.generarQR()

        return res
