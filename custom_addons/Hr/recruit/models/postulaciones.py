from odoo import fields, models, api

class postulaciones(models.Model):
    _name = 'recruit.postulaciones'
    _description = 'postulaciones'

    name = fields.Char()

    formacion = fields.Char(string='Formacion', required=False)
    experiencia = fields.Integer(string='Experiencia en años', required=False)
    conocimiento = fields.Char(string='Cónocimiento', required=False)
    departamento = fields.Many2one(comodel_name='hr.department', string='Departamento', required=False,
                                      store=True)
    postulantes_id = fields.Many2many(comodel_name='recruit.postulantes', string='Postulantes', required=False,
                                      store=True)
    tipo_contraro = fields.Selection(
        string='Tipo de contrato',
        selection=[('eventual', 'Contrato eventual'),
                   ('parcial', 'Contrato tiempo parcial'),
                   ('servicios', 'Servicios Profesionales'),
                   ('tiempocompleto', 'Contrato Tiempo completo'), ],
        required=False, )

    inico_postulacion = fields.Datetime(string='Inicio de Postulacion', required=False)
    fin_postulacion = fields.Datetime(string='Fin de postulación', required=False)

    actividades_id = fields.Many2many(
        comodel_name='recruit.actividades',
        string='Actividades')

    conocimientoespecifico_id = fields.Many2many(
        comodel_name='recruit.conocimientoespecifico',
        string='Conocimientos especificos')

    habilidades_id = fields.Many2many(
        comodel_name='recruit.habilidades',
        string='Habilidades')

    #postulante_id = fields.Many2one(comodel_name='hr.', string='Empleado', required=False,
    #                                compute='_establecer_empleado', store=True)




