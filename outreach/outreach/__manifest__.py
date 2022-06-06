# -*- coding: utf-8 -*-
{
    'name': "outreach",
    'summary': """
        Module to manage Outreach Clinic statistics for SAN-KER""",
    'description': """
        Module to manage Outreach Clinics statistics for SAN-KER
    """,
    'author': "Gideon Rynjah",
    'website': "http://www.san-ker.org",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sanker'],

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