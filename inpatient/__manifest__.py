# -*- coding: utf-8 -*-
{
    'name': "InPatient Module",
    'summary': """Module for managing In-Patient Admissions at San-Ker""",
    'description': """To integrate Inpatient Management""",
    'author': "Gideon Rynjah",
    'website': "http://www.san-ker.org",
    'category': 'Healthcare',
    'version': '0.1',
    'depends': ['base','sale','sanker'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/views1.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,

}
