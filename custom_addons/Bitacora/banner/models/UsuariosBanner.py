import json
from datetime import datetime

import requests

from odoo import fields, models, api


class UsuarioBanner(models.Model):
    _name = 'banner.usuarios'
    _description = 'Usuario de Banner'

    name = fields.Char(compute='_compute_name', store=True, string="Nombre Completo")

    pidm = fields.Char(string='PIDM', required=False)
    banner_id = fields.Char(string='Banner ID', required=False)
    cedula = fields.Char(string='Cédula', required=False)
    claim = fields.Char(string='PUCE Claim', required=False)
    username = fields.Char(string='Nombre de Usuario', required=False)
    pin = fields.Char(string='PIN', required=False)
    nombres = fields.Char(string='Nombres', required=False)
    apellidos = fields.Char(string='Apellidos', required=False)
    correo = fields.Char(string='Correo', required=False)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for user in self:
            user.name = f"{user.apellidos} {user.nombres}"

    def enviarCorreo(self):
        template = self.env.ref("banner.notificacion_credenciales_mt").id
        for rec in self:
            if rec.correo:
                self.env["mail.template"].sudo().browse(template).send_mail(rec.id, force_send=True)

    @api.model
    def obtenerUsuarios(self):

        url = f"https://user_sdo:BTq[4@M9$kL3@pucewsd.puce.edu.ec/usuario/datosUsuario/E5DSjP2" \
              f"?fecha_inicio=1970-01-01&fecha_fin={datetime.now().strftime('%Y-%m-%d')}"

        response = requests.get(url, verify=False)
        data = json.loads(response.content)

        model = self.env['banner.usuarios']
        users = model.search([])
        users.unlink()

        for user in data['USER']:
            model.create({
                'pidm': user['PIDM'],
                'banner_id': user['ID_BANNER'],
                'cedula': user['NUMDOC'],
                'claim': user['PUCE_CLAIM'],
                'username': user['USERNAME'],
                'pin': user['PIN'],
                'nombres': f"{user['PRIMER_NOMBRE']} {user['SEGUNDO_NOMBRE']}",
                'apellidos': f"{user['PRIMER_APELLIDO']} {user['SEGUNDO_APELLIDO']}",
                'correo': f"{user['USERNAME'].lower()}@pucesd.edu.ec",
            })
