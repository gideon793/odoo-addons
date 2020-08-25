# -*- coding: utf-8 -*-
{
    'name': "diagnosis",
    'summary': """Diagnosis as Per ICD classification""",
    'description': """Diagnosis as Per ICD classification""",
    'author': "Gideon Rynjah",
    'website': "http://www.san-ker.org",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
}