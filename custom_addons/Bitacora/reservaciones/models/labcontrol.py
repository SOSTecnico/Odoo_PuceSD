import threading

from odoo import fields, models, api

import socketio
import eventlet

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)

def start_socket_server():
    eventlet.wsgi.server(eventlet.listen(('', 6969)), app)


t = threading.Thread(target=start_socket_server)

t.start()


class Computadoras(models.Model):
    _name = 'reservaciones.computadoras'
    _description = 'Description'

    name = fields.Char(string="Nombre")
    ip = fields.Char(string='Dirección IP', required=False)
    estado = fields.Selection(string='Estado', selection=[('online', 'ONLINE'), ('offline', 'OFFLINE'), ],
                              required=False, )
    action = fields.Char(string='Acción', required=False, )

    @sio.event
    def connect(sid, environ, auth):
        print('connect ', sid)

    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)