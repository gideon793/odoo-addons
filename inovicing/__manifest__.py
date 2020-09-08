# -*- coding: utf-8 -*-
{
	'name': 'Invoicing',
	'version': '0.1',
	'summary': 'Editing the invoices for IP Billing',
	'category': 'Healthcare',
	'author': 'Gideon Rynjah',
	'maintainer': 'SAN-KER',
	'company': 'SAN-KER',
	'website': 'http://www.san-ker.org',
	'depends': ['base','account','sale','purchase'],
	'data': [
        'views/views.xml',
		'security/ir.model.access.csv'
    ],
	'images': [],
	'license': 'AGPL-3',
	'installable': True,
	'application': True,
	'auto_install': False,
}