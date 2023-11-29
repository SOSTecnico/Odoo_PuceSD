# -*- coding: utf-8 -*-
{
    'name': "reservas",

    'summary': """Actualizacion del modulo reservaciones""",

    'description': """
        Nuevo modulo para mejorar las reservas en los laboratorios de computo
    """,

    'author': "Ricardo Arias, Bryan Castillo, Richard Arboleda",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '2.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menuitem.xml',
        'views/templates.xml',
        'views/reservasview.xml',
        'views/website/formulario.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
