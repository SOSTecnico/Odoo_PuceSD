
from odoo import http
from odoo.http import request

class Recruit(http.Controller):
    @http.route('/postulantes/formulario', auth='public', website= True)
    def index(self, **kw):
        prod_obj = request.env['recruit.postulaciones'].sudo().search([])
        return request.render("recruit.formulario_recruit_template",{
            "resul": prod_obj
        })