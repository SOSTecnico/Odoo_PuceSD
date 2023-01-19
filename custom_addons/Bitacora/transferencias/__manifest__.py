# -*- coding: utf-8 -*-

{
    'name': "Transferencias de Activos Fijos",

    'summary': """
        Módulo para llevar el control de las transferencias de Activos Fijos""",

    'description': """
        En este módulo se puede llevar el registro de todos los movimientos y custodios de los activos fijos
    """,

    'author': "Jonathan Moreno",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail','web_m2x_options'],

    # always loaded
    'data': [
        'security/roles.xml',
        'security/ir.model.access.csv',
        'data/TiposTransferencia.xml',
        'views/MainMenu.xml',
        'views/Marcas.xml',
        'views/Ubicaciones.xml',
        'views/Responsables.xml',
        'views/Activos.xml',
        'views/Transferencias.xml',
        'views/TipoTransferencias.xml',
        'views/Prestamos.xml',
        'reports/Transferencias.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
