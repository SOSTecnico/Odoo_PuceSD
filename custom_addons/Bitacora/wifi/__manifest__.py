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
    'assets': {
        'web.assets_backend': {
            'wifi/static/src/js/tree_buttons.js',
            'wifi/static/src/js/docentes_tree_button.js',
        },
        'web.assets_frontend':{
            'wifi/static/src/js/docentes_copy_clipboard.js'
        },
        'web.assets_qweb': {
            'wifi/static/src/xml/tree_buttons.xml',
            'wifi/static/src/xml/docentes_buttons_tree.xml',
        }
    },
    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],
    # always loaded
    'data': [
        'data/Parametros.xml',
        'security/Roles.xml',
        'security/ir.model.access.csv',
        'views/MainMenu.xml',
        'views/EstudiantesWifi.xml',
        'views/Configuraciones.xml',
        'views/DocentesWifi.xml',
    ],
    # only loaded in demonstration mode
}
