# -*- coding: utf-8 -*-
{
    'name': "SAN-KER Employee Management",

    'summary': """
        Employee Management Module for SAN-KER""",

    'description': """
        Employee Management Module for SAN-KER
    """,

    'author': "Gideon Rynjah",
    'website': "http://www.san-ker.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Healthcare',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
        'views/views1.xml',
        'views/views2.xml',
        'views/contractview.xml'
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}