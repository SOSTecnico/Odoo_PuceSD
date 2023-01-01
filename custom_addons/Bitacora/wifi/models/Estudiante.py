from odoo import fields, models, api
from odoo.http import request
import mysql.connector
from mysql.connector import Error

from odoo.exceptions import ValidationError


class WifiDB:

    def __init__(self):
        try:
            config = self.obtener_parametros_conexion_radius()

            self.conexion = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                user=config['db_user'],
                password=config['db_password'],
                db=config['db_name']
            )
        except Error as ex:
            raise ValidationError(f"Ocurrió un error al conectarse a la Base de Datos: {ex}")

    def obtener_parametros_conexion_radius(self):
        configuracion = request.env['wifi.configuracion'].search_read([('clave', 'like', 'radius')],
                                                                      fields=['clave', 'value'])
        config = {}
        for c in configuracion:
            if c['clave'] == 'radius_host':
                config['host'] = c['value']
            if c['clave'] == 'radius_port':
                config['port'] = c['value']
            if c['clave'] == 'radius_db_name':
                config['db_name'] = c['value']
            if c['clave'] == 'radius_db_user':
                config['db_user'] = c['value']
            if c['clave'] == 'radius_db_password':
                config['db_password'] = c['value']
        return config

    def obtener_usuarios(self):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor(dictionary=True)
                cursor.execute("""SELECT * FROM radcheck""")
                result = cursor.fetchall()

                return result
            except Error as ex:
                raise ValidationError(f"Ocurrió un error al Obtener Usuarios: {ex}")

    def actualizar_usuarios(self, parameters):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = """INSERT INTO radcheck (id,identity,username,attribute,
                                            op,value,name,last_name,email,
                                            `career-unit`,`period-position`,
                                            date,status,expire)
                                            VALUES (0,%s,%s,'Cleartext-Password',':=',%s,%s,%s,%s,%s,NULL,CURDATE(),1,NULL)
                        ON DUPLICATE KEY UPDATE identity=%s,username=%s, value=%s, name=%s,
                                                last_name=%s, email=%s, `career-unit`=%s"""

                cursor.executemany(sql, parameters)
                self.conexion.commit()
                result = cursor.rowcount
                return result
            except Error as ex:
                raise ValidationError(f"Ocurrió un error al Actualizar Usuarios: {ex}")

    def eliminar_usuarios(self, values):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                print(values)
                cursor.executemany("""DELETE FROM radcheck WHERE username = %s""", values)
                self.conexion.commit()
                result = cursor.rowcount
                return result
            except Error as ex:
                raise ValidationError(f"Ocurrió un error al Eliminar Usuarios: {ex}")


class EstudianteWifi(models.Model):
    _name = 'wifi.estudiantes'
    _description = 'Wifi Estudiante'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute="_compute_name", store=True, string="Nombre")
    nombres = fields.Char(string='Nombres', required=True, tracking=True)
    apellidos = fields.Char(string='Apellidos', required=True, tracking=True)
    cedula = fields.Char(string='Cédula', required=True, tracking=True)
    username = fields.Char(string='Usuario', required=True, tracking=True)
    email = fields.Char(string='Correo', required=False, tracking=True, compute='_compute_email', store=True)
    carrera = fields.Char(string='Carrera', required=False, tracking=True)
    password = fields.Char(string='Contraseña', required=False, tracking=True)

    @api.depends('username')
    def _compute_email(self):
        for usuario in self:
            if usuario.username:
                usuario.email = f"{usuario.username}@pucesd.edu.ec"

    @api.depends('nombres', 'apellidos')
    def _compute_name(self):
        for usuario in self:
            usuario.name = f"{usuario.nombres} {usuario.apellidos}"

    @api.onchange('cedula')
    def _onchange_cedula(self):
        if self.cedula:
            self.password = self.cedula

    @api.model
    def recuperar_usuarios_desde_radius(self):
        print("iniciando sincronización...")
        radius = WifiDB()
        usuarios = radius.obtener_usuarios()
        usuarios_wifi = self.search([]).mapped('username')
        for usuario in usuarios:
            if not usuario['username'] in usuarios_wifi:
                self.create({
                    'username': usuario['username'],
                    'nombres': usuario['name'],
                    'apellidos': usuario['last_name'],
                    'cedula': usuario['identity'],
                    'password': usuario['value'],
                    'email': usuario['email'],
                    'carrera': usuario['career-unit'],
                })

    def sincronizar_usuarios(self):
        print("Actualizando Usuarios")
        radius = WifiDB()
        usuarios = []
        for usuario in self:
            # No cambiar el orden de los parametros, caso contrario cambiar la consulta en la Clase WifiDB
            usuarios.append(
                (usuario.cedula, usuario.username, usuario.password, usuario.nombres, usuario.apellidos, usuario.email,
                 usuario.carrera, usuario.cedula, usuario.username, usuario.password, usuario.nombres,
                 usuario.apellidos, usuario.email,
                 usuario.carrera))
        result = radius.actualizar_usuarios(usuarios)
        print("Cantidad de Filas Afectadas ", result)

    def unlink(self):
        usuarios = []
        for u in self:
            usuarios.append((u.username,))
        res = super(EstudianteWifi, self).unlink()
        radius = WifiDB()
        radius.eliminar_usuarios(usuarios)
        return res
