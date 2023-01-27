# -*- coding: utf-8 -*-
{
    'name': "Control de Asistencias",

    'summary': """
        Módulo para controlar el registro de asistencias del personal""",

    'description': """
        Esta aplicación permite monitorear y controlar las asistencias de los empleados, revisar los atrasos, permisos,
        vacaciones entre otros parámetros relacionados con la asistencia.
    """,

    'author': "Jonathan Moreno",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr', 'web_m2x_options'],
    'assets': {
        'web.assets_backend': {
            'racetime/static/src/js/marcaciones.js',
        },
        'web.assets_qweb': {
            'racetime/static/src/xml/marcaciones.xml',
        }
    },
    # always loaded
    'data': [
        'data/Parametros.xml',
        'security/Grupos.xml',
        'security/ir.model.access.csv',
        'views/MainMenu.xml',
        'views/Feriados.xml',
        'views/TiposPermiso.xml',
        'views/Permisos.xml',
        'views/Empleados.xml',
        'views/Vacaciones.xml',
        'views/Horas.xml',
        'views/Config.xml',
        'views/Horarios.xml',
        'views/ReporteMarcaciones.xml',
        'views/DetalleMarcaciones.xml',
        'views/CronMarcaciones.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
