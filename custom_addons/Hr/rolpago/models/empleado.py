from odoo import fields, models, api
from datetime import datetime, timedelta

import requests


class Empleado(models.Model):
    _inherit = 'hr.employee'
    _description = 'Description'

    codigo_sap = fields.Char(
        string='Codigo_sap', 
        required=False)


    def generar_rol(self):

        fecha = datetime.today().replace(day=1) - timedelta(days=1)

        self.env['rolpago.roles'].sudo().search(
            [('empleado_id', '=', self.id), ('fecha', 'like', f"{fecha.strftime('%Y-%m')}")]).unlink()

        headers = {'charset': 'UTF-8', 'Content-Type': 'json'}

        url = f"https://pucesapwd.puce.edu.ec:44400/RESTAdapter/RoldePago/{self.identification_id}?tipdoc=01&mes={fecha.strftime('%m')}&ano={fecha.strftime('%Y')}&socie=6000"
        data = requests.get(url, headers, auth=('POP_WS', 'Puc3S4p1')).json()

        if data['MT_IHR006_RoldePago_Out_Resp']['Log']['TipoMensaje'] != 'E':
            rubros = data['MT_IHR006_RoldePago_Out_Resp']['Detalle']
            model_rubros = []
            for rubro in rubros:
                model_rubros.append((0, 0, {
                    'descripcion': rubro['TextoConcepto'],
                    'valor': rubro['Monto'],
                    'horas_laborables': rubro['Horas'],
                    'tipo': 'ingreso' if rubro['Signo'] == '+' else 'egreso',
                }))

            self.env['rolpago.roles'].sudo().create({
                'empleado_id': self.id,
                'fecha': fecha.strftime("%Y-%m-%d"),
                'rubros_id': model_rubros
            })