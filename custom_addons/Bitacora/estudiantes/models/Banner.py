from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'ProjectName.TableName'
    _description = 'Description'

    pidm = fields.Char(
        string='PIDM',
        required=False)

    id_banner = fields.Char(
        string='ID BANNER',
        required=False)

    codigosap = fields.Char(
        string='CODSAP',
        required=False)

    tipodedocumento = fields.Char(
        string='TIPO DE DOCUMENTO',
        required=False)

    numerodedocumento = fields.Char(
        string='NUMERO DE DOCUMENTO',
        required=False)

    puceclaim = fields.Char(
        string='PUCECLAIM',
        required=False)

    nombredeusuario = fields.Char(
        string='NOMBRE DE USUARIO',
        required=False)

    pin = fields.Char(
        string='COMTRASEÑA',
        required=False)

    tipo_persona = fields.Char(
        string='ID BANNER',
        required=False)