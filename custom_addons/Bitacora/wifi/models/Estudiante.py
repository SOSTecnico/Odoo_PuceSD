from odoo import fields, models, api
import mysql.connector
from mysql.connector import Error

from odoo.exceptions import ValidationError
from odoo.tools import config


class WifiDB:

    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host=config.get('wifi_host'),
                port=config.get('wifi_port'),
                user=config.get('wifi_user'),
                password=config.get('wifi_password'),
                db=config.get('wifi_db_name')
            )
        except Error as ex:
            raise ValidationError(f"Ocurrió un error al conectarse a la Base de Datos: {ex}")

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
