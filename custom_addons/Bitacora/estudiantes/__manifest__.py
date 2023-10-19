# -*- coding: utf-8 -*-
{
    'name': "Estudiantes",

    'summary': """
        Este módulo recopila información General sobre los estudiantes de la PUCESD""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jonathan Moreno",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'School',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/Groups.xml',
        'security/ir.model.access.csv',
        'views/MainMenu.xml',
        'views/Carreras.xml',
        'views/Estudiantes.xml',
        'views/Config.xml',
        'views/EmailTemplates/CredencialesPortas.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
