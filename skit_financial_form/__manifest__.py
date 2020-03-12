# -*- coding: utf-8 -*-

{
    'name': 'Ahorasoft Aux Reporting',
    'version': '1.3',
    'summary': 'Modulo auxiliar para reportes.',
    'author': 'Ahorasoft',
    'website': 'http://www.ahorasoft.com',
    'description': """
        Modulo auxiliar para reportes.
        """,
    # 'images': ['images/main_screenshot.png'],
    'category': "Accounting",
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_financial_report_data.xml',
        'views/account_menuitem.xml',
        'views/account_view.xml',   
    ],
    'installable': True,    
    'auto_install': False,
    'application': True,
}
