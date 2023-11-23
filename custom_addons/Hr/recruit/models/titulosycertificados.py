from odoo import fields, models, api


class Titulosycertificados(models.Model):
    _name = 'recruit.titulosycertificados'
    _description = 'Description'

    name = fields.Char()
    titulo = fields.Char(
        string='Titulo Obtenido',
        required=False)

    pais = fields.Char(
        string='Pais',
        required=False)

    institucion = fields.Char(
        string='Institucion',
        required=False)

    tiempoformacion = fields.Char(
        string='Tiempo formacion',
        required=False)

    numeroregistrocenecit = fields.Char(
        string='Numerore gistro cenecit',
        required=False)

    fechagraduacion = fields.Date(
        string='Fecha de graduacion',
        required=False)

    fechainicio = fields.Date(
        string='Fecha Inicio',
        required=False)

    fechafin = fields.Date(
        string='Fecha finalizacion',
        required=False)
