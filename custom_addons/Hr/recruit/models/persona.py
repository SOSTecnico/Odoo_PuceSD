from odoo import fields, models, api


class Persona(models.AbstractModel):
    _name = 'recruit.persona'
    _description = 'Description'

    cedula = fields.Char(
        string='Numero de Cedula',
        required=False)

    nombres = fields.Char(
        string='Nombres',
        required=False)

    apellidos = fields.Char(
        string='Apellidos',
        required=False)

    genero = fields.Selection(
        string='Genero',
        selection=[('masculino', 'Masculino'),
                   ('femenino', 'Femenino'),
                   ('otros', 'Otro'), ],
        required=False)

    correo = fields.Char(
        string='Correo',
        required=False)

    estadocivil = fields.Selection(
        string='Estado civil',
        selection=[('soltero', 'Soltero'),
                   ('casado', 'Casado'),
                   ('divorciado', 'Divorciado'),
                   ('viudo', 'Viudo'), ],
        required=False)

    direccion = fields.Text(
        string='Direccion',
        required=False)

    fecha_nacimiento = fields.Date(
        string='Fecha de nacimiento',
        required=False)

    nacionalidad = fields.Many2one(
        comodel_name='res.country',
        string='Nacionalidad',
        required=False)

    provincia = fields.Many2one(
        comodel_name='res.country.state',
        string='Provincia',
        required=False)

    lugar_nacimiento = fields.Char(
        string='Lugar de Nacimiento',
        required=False)

    tiposangre = fields.Selection(
        selection=[('O+', 'O+'),
                   ('O-', 'O-'),
                   ('A+', 'A+'),
                   ('A-', 'A-'),
                   ('AB+', 'AB+'),
                   ('AB-', 'AB-'), ],
        required=False)

    celular = fields.Char(
        string='Celular',
        required=False)

    telefono_fijo = fields.Char(
        string='Numero de telefono',
        required=False)




