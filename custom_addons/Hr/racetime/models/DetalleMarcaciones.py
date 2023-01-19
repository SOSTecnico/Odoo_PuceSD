from psycopg2 import Error

from odoo import fields, models, api
import pyodbc

from odoo.exceptions import ValidationError
from odoo.http import request


class Biotime:
    def __init__(self):
        try:
            config = self.obtener_parametros_conexion_biotime()

            self.conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL server}; SERVER=' + config['host'] +
                ';DATABASE=' + config['db_name'] +
                ';UID=' + config['db_user'] +
                ';PWD=' + config['db_password'])
        except Error as ex:
            raise ValidationError(f"Ocurrió un error al conectarse a la Base de Datos: {ex}")

    def obtener_marcaciones(self, sql):
        cursor = self.conexion.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conexion.commit()
        cursor.close()
        return result


    def obtener_parametros_conexion_biotime(self):
        configuracion = request.env['racetime.config'].search_read([('key', 'like', 'biotime')],
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
    fecha_hora = fields.Datetime(string='Fecha y Hora', required=False)
    id_empleado = fields.Integer(string='ID Empleado', required=False)
    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado', required=False)



    # def obtener_marcaciones(self):
    #     sql = """SELECT * FROM iclock_transaction"""
    #     result = Biotime().obtener_marcaciones(sql)
    #     empleados = self.env['hr.employee'].search()
    #
    #     for row in result:
    #         empleados.search([('emp_code')])
    #         self.create({
    #             'fecha_hora': row.punch_time,
    #             'id_empleado':row.emp_code,
    #             'empleado_id':
    #
    #         })
    #         print(row.punch_time)
