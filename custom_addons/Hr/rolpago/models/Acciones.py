from datetime import datetime, timedelta

import requests

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class RolAcciones(models.TransientModel):
    _name = 'rolpago.acciones'
    _description = 'Description'

    name = fields.Char()

    def ILG003(self):
        url = "https://pucesapwd.puce.edu.ec:44400/RESTAdapter/personal/?sociedad=6000&areap=0102"
        # url = "https://POP_WS:Puc3S4p1@pucesapwd.puce.edu.ec:44400/RESTAdapter/personal/?sociedad=6000&areap=0102"

        response = requests.get(url,
                                auth=('POP_WS', 'Puc3S4p1'))
        respuesta = response.json()
        personal = respuesta['MT_IHR003_ConsultadePersonal_Out_Resp']['DatosPersonales']

        # nuevos_empleados = self.env["hr.employee"].search([("codigo_sap","in",codigo_sap)])
        empleados = self.env["hr.employee"].search(['|', ('active', '=', True), ('active', '=', False)]).mapped(
            "codigo_sap")
        for value in personal:
            if str(value["CodSAP"]) not in empleados:
                self.env["hr.employee"].create(
                    {
                        'name': f"{value['PrimerNombre'].upper()} {value['SegundoNombre'].upper()} {value['PrimerApellido'].upper()} {value['SegundoApellido'].upper()}",
                        'codigo_sap': str(value['CodSAP']),
                        'employee_type': 'employee'
                    })

        return {
            'type': 'tree',
            'name': 'Empleados',
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'type': 'ir.actions.act_window',
            'target': 'main'
        }

    def ILG006(self):

        fecha = datetime.today().replace(day=1) - timedelta(days=1)

        # Fecha de prueba para sacar roles de otros meses
        # fecha = datetime(2023, 1, 1)

        headers = {'charset': 'UTF-8', 'Content-Type': 'json'}

        empleados = self.env['hr.employee'].sudo().search([])
        tipos_de_rubros = self.env['rolpago.tipo_rubro'].sudo().search([])
        for empleado in empleados:

            self.env['rolpago.roles'].sudo().search(
                [('estado_rol', '=', 'publicado'), ('empleado_id', '=', empleado.id),
                 ('fecha', 'like', f"{fecha.strftime('%Y-%m')}")]).unlink()

            url = f"https://pucesapwd.puce.edu.ec:44400/RESTAdapter/RoldePago/{empleado.identification_id}?tipdoc=01&mes={fecha.strftime('%m')}&ano={fecha.strftime('%Y')}&socie=6000"
            data = requests.get(url, headers, auth=('POP_WS', 'Puc3S4p1')).json()
            if data['MT_IHR006_RoldePago_Out_Resp']['Log']['TipoMensaje'] != 'E':
                rubros = data['MT_IHR006_RoldePago_Out_Resp']['Detalle']
                model_rubros = []
                for rubro in rubros:
                    tipo_rubro = tipos_de_rubros.filtered_domain([('name', '=', rubro['TextoConcepto'])])

                    model_rubros.append((0, 0, {
                        'valor': rubro['Monto'],
                        'horas_laborables': rubro['Horas'],
                        'tipo_rubro_id': tipo_rubro.id,
                    }))

                self.env['rolpago.roles'].sudo().create({
                    'empleado_id': empleado.id,
                    'fecha': fecha.strftime("%Y-%m-%d"),
                    'rubros_id': model_rubros
                })

        return {
            'type': 'tree',
            'name': 'Roles',
            'view_mode': 'tree,form',
            'res_model': 'rolpago.roles',
            'context': {'search_default_empleados_group': 2, 'search_default_estado_group': 1},
            'type': 'ir.actions.act_window',
            'target': 'main'
        }
