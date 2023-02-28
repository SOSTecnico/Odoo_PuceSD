from odoo import fields, models, api
import requests
from .empleado import Empleado
import json


class Roles(models.Model):
    _name = 'rolpago.roles'
    _description = 'Roles'

    name = fields.Char()

    empleado_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Empleado',
        required=False)

    periodo = fields.Char(
        string='Periodo',
        required=False)

    rubros_id = fields.One2many(
        comodel_name='rolpago.rubros',
        inverse_name='roles_id',
        string='Rubros_id',
        required=False)

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

    def ILG006(self):
        headers = {'charset': 'UTF-8', 'Content-Type': 'json'}
        url = "https://pucesapwd.puce.edu.ec:44400/RESTAdapter/RoldePago/1725042871?tipdoc=01&mes=11&ano=2022&socie=6000"
        # url = "https://POP_WS:Puc3S4p1@pucesapwd.puce.edu.ec:44400/RESTAdapter/personal/?sociedad=6000&areap=0102"

        response = requests.get(url, headers,
                                auth=('POP_WS', 'Puc3S4p1'))
        respuesta = response.json()

        # persona = respuesta['MT_IHR006_RoldePago_Out_Resp']['DatoPersonal']
        rubros = respuesta['MT_IHR006_RoldePago_Out_Resp']['Detalle']
        print(rubros)

    #   print(empleados)

    # for i in personal:
    #     # print(i['CodSAP'],i['PrimerApellido'],i['SegundoApellido'],i['PrimerNombre'],i['SegundoNombre'],i['AreaPersonal'],i['GrupoPersonal'])
    #     # print(i)
    #
    #     self.env["hr.employee"].create(
    #         {'name': f"{i['PrimerNombre']} {i['SegundoNombre']} {i['PrimerApellido']} {i['SegundoApellido']}",
    #          'codigo_sap': i['CodSAP'],
    #          'employee_type': 'employee'})
