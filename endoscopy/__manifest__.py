# -*- coding: utf-8 -*-
{
    'name': "Endoscopy",

    'summary': """
        Endoscopy Module for SAN-KER""",

    'description': """
        Module for creating endoscopy reports by uploading saved pictures
    """,

    'author': "Gideon Rynjah",
    'website': "http://www.san-ker.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Healthcare',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sanker','dateofbirth'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}