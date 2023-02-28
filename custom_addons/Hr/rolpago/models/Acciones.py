import requests

from odoo import fields, models, api


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
        empleados = self.env["hr.employee"].search([]).mapped("codigo_sap")
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
        headers = {'charset': 'UTF-8', 'Content-Type': 'json'}
        url = "https://pucesapwd.puce.edu.ec:44400/RESTAdapter/RoldePago/2300349640?tipdoc=01&mes=11&ano=2022&socie=6000"

        response = requests.get(url, headers,
                                auth=('POP_WS', 'Puc3S4p1'))
        respuesta = response.json()

        # persona = respuesta['MT_IHR006_RoldePago_Out_Resp']['DatoPersonal']
        rubros = respuesta['MT_IHR006_RoldePago_Out_Resp']['Detalle']
        print(rubros)
