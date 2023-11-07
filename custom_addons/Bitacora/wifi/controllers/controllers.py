# -*- coding: utf-8 -*-
from oracledb import Error

from odoo import http
from odoo.http import request


class Wifi(http.Controller):
    @http.route('/wifi/formulario', auth='user', website=True)
    def index(self, **kw):
        if request.env.user.has_group('wifi.group_admin'):
            return request.render('wifi.template_generar_usuario')
        else:
            return request.redirect('/')

    @http.route('/wifi/generar_usuarios', auth='user', website=True)
    def generar_script(self, **data):
        # Se consulta a los usuarios de banner, se busca la cedula apartado por una coma
        usuarios = request.env["banner.usuarios"].search([("cedula", "in", data["cedulas"].split(","))])
        # Mediante la condicional for a usuarios se imprime los datos que se desean aparece
        for i in usuarios:
            print(i.nombres)
            print(i.apellidos)
            print(i.pidm)
            print(i.correo)
            print(i.cedula)
        # Se retorna el pedido renderizando la vista en docentes con nombre wifi template, leyendo los datos en usuario
        return request.render('wifi.template_docentes_script', {'usuarios': usuarios.read()})
