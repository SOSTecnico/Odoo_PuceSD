# -*- coding: utf-8 -*-
{
    'name': "Wifi",

    'summary': """Módulo que permite el monitoreo y control de acceso de Usuarios Wifi en las redes para 
                docentes y Estudiantes""",

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
        'security/Roles.xml',
        'security/ir.model.access.csv',
        'views/MainMenu.xml',
        'views/EstudiantesWifi.xml',
    ],
    # only loaded in demonstration mode
}
