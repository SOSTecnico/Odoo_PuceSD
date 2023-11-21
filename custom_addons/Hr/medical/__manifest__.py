# -*- coding: utf-8 -*-
{
    'name': "Centro Médico PUCESD",

    'summary': """
        Módulo para llevar el registro de historias clinicas en el centro Médico de la PUCESD""",

    'description': """
        
    """,

    'author': "Jonathan Moreno",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Health',
    'version': '0.1',
    'assets': {
        'web.assets_frontend': {
            'medical/static/src/scss/solicitud-cita-medica.scss',
            'medical/static/src/js/solicitud-cita.js',
        }
    },

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr', 'estudiantes', 'web'],

    # always loaded
    'data': [
        'security/Groups.xml',
        'security/ir.model.access.csv',
        'views/MainMenu.xml',
        'views/Alergias.xml',
        'views/HistoriaClinica.xml',
        'views/Consulta.xml',
        'views/Pacientes.xml',
        'views/ContactoEmergencia.xml',
        'views/Cie10.xml',
        'views/Citas.xml',
        'views/Horario.xml',
        #     DATA
        'data/HorarioDefault.xml',
        #   Email Templates
        'views/EmailTemplates/ConfirmacionCita.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
