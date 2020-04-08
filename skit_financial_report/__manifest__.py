# -*- coding: utf-8 -*-

{
    'name': 'Ahorasoft Pivote Financiero',
    'version': '1.4',
    'author': 'Ahorasoft',
    'website': 'http://www.ahorasoft.com',
    'summary': 'Pivote Financiero',
    'description': """
            Pivote Financiero
    """,
    'category': 'Accounting',
#     'images': ['images/main_screenshot.png'],
    'depends': ['account','skit_financial_form'],
    'data': [
            'views/report_wizard.xml',
            'views/account_menus.xml',
            'views/profit_loss_report_view.xml',
            'views/balance_sheet_report_view.xml',
            'security/ir.model.access.csv',
            ],
    'auto_install': False,
    'application': True,
    'installable': True,
}
