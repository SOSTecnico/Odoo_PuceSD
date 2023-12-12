import json

from datetime import datetime

import requests

from odoo import fields, models, api

from ldap3 import Server, Connection, ALL

import logging

_logger = logging.getLogger(__name__)


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
    notifi = fields.One2many(string='Notificaciones', comodel_name='banner.historial_notificacion',
                             inverse_name='usuario')
    facultad = fields.Char(string='Facultad', required=False)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for user in self:
            user.name = f"{user.apellidos} {user.nombres}"

    def enviarCorreo(self):
        template = self.env.ref("banner.notificacion_credenciales_mt").id
        for rec in self:
            if rec.correo:
                self.env["mail.template"].sudo().browse(template).send_mail(rec.id, force_send=True)
                print(rec.id)
                self.env["banner.historial_notificacion"].create({"fecha": datetime.now(), "usuario": rec.id})

    @api.model
    def obtenerUsuarios(self):

        url = f"https://user_sdo:BTq[4@M9$kL3@pucewsd.puce.edu.ec/usuario/datosUsuario/E5DSjP2" \
              f"?fecha_inicio=1970-01-01&fecha_fin={datetime.now().strftime('%Y-%m-%d')}"

        response = requests.get(url, verify=False)
        data = json.loads(response.content)

        model = self.env['banner.usuarios']
        users = model.search([]).mapped('cedula')

        for user in data['USER']:
            if not user['NUMDOC'] in users:
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
                    'facultad': user['FACULTAD']
                })

        modelBiblioteca = self.env['biblioteca.usuarios']
        usersBiblioteca = modelBiblioteca.search([]).mapped('cedula')

        for u in data['USER']:
            if not u['NUMDOC'] in usersBiblioteca:
                modelBiblioteca.create({
                    'cedula': u['NUMDOC'],
                    'nombres': f"{u['PRIMER_NOMBRE']} {u['SEGUNDO_NOMBRE']}",
                    'apellidos': f"{u['PRIMER_APELLIDO']} {u['SEGUNDO_APELLIDO']}",
                    'email': f"{u['USERNAME'].lower()}@pucesd.edu.ec",
                    'carrera': u['FACULTAD']
                })

    @api.onchange('pin')
    def onchange_pin(self):
        if self.pin:
            try:
                server = Server('192.168.250.23', get_info=ALL, use_ssl=True)
                conn = Connection(server, user='nemesis', password='825374200', auto_bind=True)

                conn.search('ou=pucesd,dc=pucesd,dc=edu,dc=ec', f'(description={self.cedula})')

                if conn.entries:
                    user = conn.response[0]
                    conn.extend.microsoft.modify_password(user.get('dn'), self.pin, old_password=None)
                    _logger.info('Se ha cambiado la contraseña de Banner Exitosamente!!!')
                    _logger.info(f'Usuario: {self.name} - {self.cedula}')
            except Exception as e:
                print(e)
                _logger.info('No se pudo cambiar la contraseña')
