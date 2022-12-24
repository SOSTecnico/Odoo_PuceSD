# -*- coding: utf-8 -*-
{
    'name': "Usuarios WIFI Eduroam",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
    'depends': ['base', 'mail', 'web_m2x_options'],
    'assets': {
        'web.assets_frontend': {
            'eduroam/static/src/js/eduroam.js'
        }
    },
    # always loaded
    'data': [
        'security/Roles.xml',
        'security/ir.model.access.csv',
        'views/Usuarios.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
