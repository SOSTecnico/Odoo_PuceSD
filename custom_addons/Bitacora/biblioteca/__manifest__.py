# -*- coding: utf-8 -*-
{
    'name': "Biblioteca",

    'summary': """Este módulo permite llevar un registro de las personas que ingresan a biblioteca""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jonathan Moreno",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/Grupos.xml',
        'security/ir.model.access.csv',
        'views/Menu.xml',
        'views/Usuarios.xml',
        'views/Ingresos.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
