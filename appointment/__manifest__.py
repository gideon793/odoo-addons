# -*- coding: utf-8 -*-
{
    'name': "appointment",
    'summary': """Appointment app""",
    'description': """Appointment app    """,
    'author': "Gideon",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','sanker'],
    'application': True,
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