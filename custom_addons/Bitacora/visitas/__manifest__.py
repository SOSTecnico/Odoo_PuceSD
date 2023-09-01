# -*- coding: utf-8 -*-
{
    'name': "Visitas",

    'summary': """
        Este módulo permite generar visitas para los ingresos a la PUCESD""",

    'description': """
        En este módulo, se podrá generar visitas para que los guardias de seguridad puedan revisar quien está autorizado 
        a ingresar a la PUCESD 
    """,

    'author': "Jonathan Moreno",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Security',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr','mail'],

    # always loaded
    'data': [
        'security/Groups.xml',
        'security/ir.model.access.csv',
        'views/Menu.xml',
        'views/Visitantes.xml',
        'views/Visitas.xml',
        'views/EmailTemplates/QREmail.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
