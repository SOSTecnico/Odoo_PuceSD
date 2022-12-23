# -*- coding: utf-8 -*-

from odoo import models, fields, api
import oracledb


class OracleUsuarios:

    def execute_query(self, query):
        connection = oracledb.connect(user="QUERY_PUCESDO", password="l2UY656_", dsn="172.31.2.61:5061/PROD")

        # Se crea el cursor
        cursor = connection.cursor()
        # Se realiza la consulta, la cual se devuelve en forma de Tuplas
        cursor.execute(query)
        # Para generar el resultado en forma de DICT
        columns = [col[0] for col in cursor.description]
        cursor.rowfactory = lambda *args: dict(zip(columns, args))
        # Se devuelve el resultado de la consulta
        return cursor.fetchall()


class UsuariosWifi(models.Model):
    _name = 'eduroam.usuarios'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Usuario con acceso Wifi EDUROAM'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    email = fields.Char(string='Email', required=False, tracking=True)
    username = fields.Char(string='Nombre de Usuario', required=False, tracking=True)
    password = fields.Char(string='Contraseña', required=False, tracking=True)
    pidm = fields.Char(string='PIDM', required=False, tracking=True)
    cedula = fields.Char(string='Cédula', required=False, tracking=True)

    def obtener_usuarios(self, cedulas):
        sql = f"""SELECT spri.SPRIDEN_FIRST_NAME AS primer_nombre,spri.SPRIDEN_MI AS segundo_nombre, 
                spri.SPRIDEN_LAST_NAME AS apellidos, SP.SPBPERS_PIDM AS pidm, SP.SPBPERS_SSN AS cedula,
                GM.GOREMAL_EMAIL_ADDRESS AS correo
                FROM SPBPERS sp JOIN SPRIDEN spri ON spri.SPRIDEN_PIDM = sp.SPBPERS_PIDM  
                JOIN GOREMAL gm ON sp.SPBPERS_PIDM = GM.GOREMAL_PIDM 
                WHERE SP.SPBPERS_SSN  IN ({','.join(f"'{cedula}'" for cedula in cedulas)})
                AND (GM.GOREMAL_EMAIL_ADDRESS LIKE('%@PUCESD.EDU.EC') 
                OR GM.GOREMAL_EMAIL_ADDRESS LIKE('%@pucesd.edu.ec'))"""

        usuarios_eduroam = OracleUsuarios().execute_query(sql)

        return usuarios_eduroam
