# -*- coding: utf-8 -*-
{
    'name': "Sync Image Product",
    'summary': """
        module to migrate image from any version of Odoo""",
    'description': """
        module to migrate image from any version of Odoo
    """,
    'author': "Gt Alchemy Development",
    'license': 'LGPL-3',
    'support': 'developmentalchemygx@gmail.com',
    'price': 5.00,
    'currency': 'USD',
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_sync.xml',
    ],
}
