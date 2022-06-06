# -*- coding: utf-8 -*-
{
	'name': 'Patient details',
	'version': '0.2',
	'summary': 'Patient information',
	'category': 'Healthcare',
	'author': 'Gideon Rynjah',
	'maintainer': 'SAN-KER',
	'company': 'SAN-KER',
	'website': 'http://www.san-ker.org',
	'depends': ['base'],
	'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/patient.xml',
        'security/ir.model.access.csv',
    ],
	'images': [],
	'license': 'AGPL-3',
	'installable': True,
	'application': True,
	'auto_install': False,
}
