# -*- coding: utf-8 -*-
{
    'name': "Reservaciones",

    'summary': """Módulo para realizar reservaciones""",

    'description': """
        Módulo para realizar reservaciones
    """,

    'author': "Jonathan Moreno",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'web_m2x_options', 'hr'],
    'assets': {
        'web.assets_backend': {
            'reservaciones/static/src/js/dias_widget.js',
            'reservaciones/static/src/css/dias_widget.css',
        },
        'web.assets_qweb': {
            'reservaciones/static/src/xml/dias_widget.xml'
        }
    },
    # always loaded
    'data': [
        'security/Roles.xml',
        'security/ir.model.access.csv',
        'views/MainMenu.xml',
        'views/Escuelas.xml',
        'views/Eventos.xml',
        'views/Recursos.xml',
        'views/Requerimientos.xml',
        'views/Reservas.xml',
        'views/Usuarios.xml',
        'views/Ingresos.xml',
        # 'views/LabControl.xml',
        'views/templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
