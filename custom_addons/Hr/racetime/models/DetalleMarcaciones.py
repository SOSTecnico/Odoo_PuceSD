from psycopg2 import Error

from odoo import fields, models, api
import psycopg2

from odoo.exceptions import ValidationError
from odoo.http import request


class Biotime:
    def __init__(self):
        try:
            config = self.obtener_parametros_conexion_biotime()

            self.conexion = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                user=config['db_user'],
                password=config['db_password'],
                dbname=config['db_name']
            )
        except Error as ex:
            raise ValidationError(f"Ocurrió un error al conectarse a la Base de Datos: {ex}")

    def execute_query(self,sql,parameters):
        cursor = self.conexion.cursor()
        cursor.execute(sql,parameters)
        result = cursor.fetchall()
        self.conexion.commit()
        cursor.close()
        return result

    def obtener_parametros_conexion_biotime(self):
        configuracion = request.env['racetime.config'].search_read([('key', 'like', 'radius')],
                                                                   fields=['key', 'value'])
        config = {}
        for c in configuracion:
            if c['key'] == 'biotime_host':
                config['host'] = c['value']
            if c['key'] == 'biotime_port':
                config['port'] = c['value']
            if c['key'] == 'biotime_db_name':
                config['db_name'] = c['value']
            if c['key'] == 'biotime_db_user':
                config['db_user'] = c['value']
            if c['key'] == 'biotime_db_password':
                config['db_password'] = c['value']
        return config


class DetalleMarcacion(models.Model):
    _name = 'racetime.detalle_marcacion'
    _description = 'Detalle Marcacion'

    name = fields.Char()
    fecha_hora = fields.Datetime(string='Fecha y Hora', required=True)
    id_empleado = fields.Integer(string='ID Empleado', required=False)
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=False)
    
    def obtener_marcaciones(self):
        sql = """SELECT * FROM iclock_transaction WHERE """
        Biotime.execute_query()