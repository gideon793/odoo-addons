# -*- coding: utf-8 -*-
{
	'name': 'IP billing',
	'version': '0.1',
	'summary': 'Editing the sales order form for IP Billing',
	'category': 'Healthcare',
	'author': 'Gideon Rynjah',
	'maintainer': 'SAN-KER',
	'company': 'SAN-KER',
	'website': 'http://www.san-ker.org',
	'depends': ['base','sale'],
	'data': ['views/views.xml','views/ipbillreport.xml','views/ipbill_template.xml'],
	'license': 'AGPL-3',
	'installable': True,
	'application': True,
	'auto_install': False,
        'external_dependencies': {
        'python' : ['num2words'],

    },
}
