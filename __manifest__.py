# -*- coding: utf-8 -*-

{
    'name': 'Bancard Payment Acquirer',
    'category': 'Accounting/Payment',
    'summary': 'Payment Acquirer: Bancard Implementation',
    'version': '1.0',
    'description': """Bancard Payment Acquirer flow to allow
the testing of successful payments behaviors on e-commerce. It includes
a protection to avoid using it in production environment. However, do
not use it in production environment.
""",
    'depends': ['payment'],
    'data': [
        'static/src/xml/templates.xml',
        'views/payment_views.xml',
        'views/payment_bancard_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
} 
