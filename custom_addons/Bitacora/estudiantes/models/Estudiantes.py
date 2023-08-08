from urllib.request import urlopen

import pyodbc
import mysql.connector
import requests

import json
from datetime import date
import ssl


from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Carreras(models.Model):
    _name = 'estudiantes.carreras'
    _description = 'Carreras'

    name = fields.Char(string='Carrera', required=True)
    parent_id = fields.Many2one(comodel_name='estudiantes.carreras', string='Dependencia', required=False)


class Estudiantes(models.Model):
    _name = 'estudiantes.estudiantes'
    _description = 'Estudiante'
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('correo', 'unique(correo)', 'Ya existe un estudiante ingresado con esa Correo!')
    ]

    name = fields.Char(compute='_compute_name', store=True, string="Nombre Completo")

    nombres = fields.Char(string='Nombres', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos', required=True, tracking=True)
    cedula = fields.Char(string='Cédula'
                         , tracking=True)
    correo = fields.Char(string='Correo', required=False, tracking=True)
    celular = fields.Char(string='Celular', required=False, tracking=True)
    carrera_id = fields.Many2one(comodel_name='estudiantes.carreras', string='Carrera', tracking=True,
                                 domain="[('parent_id','!=',False),('name','!=','MAESTRÍAS'),('name','!=','ESPECIALIDADES')]")
    active = fields.Boolean(string='Active', required=False, default=True)
    estado_portas=fields.Boolean(string='Estado Portas', required=False, default=True, tracking=True)

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for estudiante in self:
            estudiante.name = f"{estudiante.nombres} {estudiante.apellidos}"

    @api.onchange("estado_portas")
    def estado_estudiante(self):
        estado=0 if self.estado_portas else 1

        sql = f"UPDATE mdl_pucesd_portas_2021_2021.mdl_user SET suspended = '{estado}' WHERE email = '{self.correo}';"
        self.conexionPortas(sql)


    def obtener_parametros_conexion_portas(self):

        configuracion = self.env['estudiantes.config'].sudo().search_read([('key', 'like', 'portas')],
                                                                       fields=['value'])
        portas_host,portas_port, portas_db_name, portas_db_user, portas_db_password = configuracion
        return portas_host["value"],portas_port["value"], portas_db_name["value"], portas_db_user["value"], portas_db_password["value"]

    def conexionPortas(self,sql):
        try:
            config = self.obtener_parametros_conexion_portas()

            miConexion = mysql.connector.connect(host=config[0], user=config[3], passwd=config[4], db=config[2])
            result = miConexion.cursor()
            result.execute(sql)

            values = []

            for row in result:

                values.append(dict((column[0], row[index]) for index, column in enumerate(result.description)))

            miConexion.commit()
            miConexion.close()

            return values

        except Exception as ex:
            raise ValidationError(f"Ocurrió un error al conectarse a la Base de Datos: {ex}")


    #@api.model
    def ILG001 (self):
        # Día actual
        today = date.today()
        resultados = []
        url = f"https://pucewsd.puce.edu.ec/usuario/datosUsuario/E5DSjP2?fecha_inicio=1900-01-01&fecha_fin={today}"
        # url = "https://POP_WS:Puc3S4p1@pucesapwd.puce.edu.ec:44400/RESTAdapter/personal/?sociedad=6000&areap=0102"

        response = requests.get(url,
                                auth=('user_sdo', 'BTq[4@M9$kL3'), verify=False)
        respuesta = response.json()
        resultados = []
        for value in respuesta["USER"]:
            resultados= value["USERNAME"]+"@PUCESD.EDU.EC"
        return resultados
    @api.model
    def sincronizar_estudiantes_Portas (self):
        try:
            values = []
            sql = """SELECT DISTINCT user.id as ID,user.USERNAME as USUARIO, user.SUSPENDED as ESTADO, user.firstname AS NOMBRES, user.lastname AS APELLIDOS, user.email AS CORREO, user.idnumber AS CEDULA, user.msn AS IDBANNER  
            FROM mdl_pucesd_portas_2021_2021.mdl_user as user 
            INNER JOIN mdl_pucesd_portas_2021_2021.mdl_role_assignments as rol ON (user.id = rol.userid) where rol.roleid='5';"""
            result_portas = self.conexionPortas(sql)
            correos = self.sudo().search([]).mapped('correo')


            for row in result_portas:
                if row['CORREO'] not in correos:

                    values.append({
                        'nombres' : row['NOMBRES'],
                        'apellidos' : row['APELLIDOS'],
                        'cedula' : row['CEDULA'],
                        'correo' : row['CORREO'],
                        'estado_portas' : True if row['ESTADO']==0 else False

                    })
            self.create(values)
        except Exception as e:
            raise ValidationError(f"Ocurrió un error: {e}")

class Sincronizacion(models.TransientModel):
    _name = 'estudiantes.sincronizacion'
    _description = 'Sincronizacion'

    def sincronizar_portas (self):
        self.env["estudiantes.estudiantes"].sincronizar_estudiantes_Portas()
