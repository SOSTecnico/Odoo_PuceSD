# -*- coding: utf-8 -*-
{
    'name': "rolpago",

    'summary': """
        Módulo que permite llevar el control de los roles de pago""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Miguel Villareal, Jonathan Moreno",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr','mail'],

    # always loaded
    'data': [
        'security/rolpago_security.xml',
        'security/ir.model.access.csv',
        'views/roles.xml',
        'views/rubros.xml',
        'views/empleado.xml',
        'views/Acciones.xml',
        'views/TipoRubro.xml',
        'reports/Rol.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
