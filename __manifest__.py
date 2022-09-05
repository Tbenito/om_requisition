# -*- coding: utf-8 -*-
{
    'name': "Requisition",

    'summary': "Application de requisition",

    'description': """
        Module Odoo permettant de consommer des articles avec tracking des Analytics
    """,

    'author': "Benito Muvum",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Requisition',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','hr','stock','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/requisition.xml',
    ],
    "application": True,
}
