# -*- coding: utf-8 -*-
{
    'name': "covid",

    'summary': """
        Covid-19 Research Project""",

    'description': """
        Covid-19 Research Project
    """,

    'author': "Gideon Rynjah",
    'website': "https://www.san-ker.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','diagnosis','dateofbirth'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/ipdtemplates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}