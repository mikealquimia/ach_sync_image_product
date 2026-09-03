# -*- coding: utf-8 -*-
{
    # =========================================================================
    # CAMBIA EN CADA MÓDULO NUEVO (bloque 1)
    # =========================================================================
    'name': 'ACH - Sync Image Product',
    'summary': 'Pull product images from another Odoo database into this one via XML-RPC',
    'version': '18.0.1.0.0',
    'category': 'Sales',

    # =========================================================================
    # FIJO PARA TODOS LOS MÓDULOS DE ACH ALCHEMICAL CODE — NO TOCAR
    # =========================================================================
    'author': 'ACH Alchemical Code',
    'website': 'https://apps.odoo.com/apps/modules/browse?author=ACH%20Alchemical%20Code',
    'support': 'mikealquimia@gmail.com',
    'license': 'OPL-1',

    'price': 3.00,
    'currency': 'USD',
    'images': ['static/description/banner.png'],

    # =========================================================================
    # CAMBIA EN CADA MÓDULO NUEVO (bloque 2)
    # =========================================================================
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_sync.xml',
    ],
    'demo': [
    ],
    'assets': {
    },

    # =========================================================================
    # FIJO — NO TOCAR
    # =========================================================================
    'installable': True,
    'application': False,
    'auto_install': False,
}
