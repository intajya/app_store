{
    'name': 'Accounting Merge Invoices Reports',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': "Easily merge multiple customer invoices into a single summarized PDF report with totals and payment type grouping.",
    'description': """
        Accounting Merge Invoices
        =======================

        This module allows you to merge multiple customer invoices into a single report. 
        It is useful for accounting teams and businesses that need consolidated invoice 
        information for customers.

        Key Features:
        --------------
        - Merge multiple invoices belonging to the same customer.
        - Generate a professional PDF "Merged Invoice Report".
        - Includes sequence numbering for each merged report.
        - Group and summarize invoice lines by product.
        - Display totals (per product and per payment method type).
        - Add custom payment types (Cash, Wallet, Online).
        - Support for expected currency rate field in invoices.
        - Option to exclude bank lines from reports.
        - Fully integrated with Odoo Accounting.

        Developed by: Mohamed Hamed
    """,
    'author': 'Intajya',
    'contributors': "Mohamed Hamed  <mhmd.hmd372017@gmail.com>",
    'depends': ['accountant', 'account_reports', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'report/paperformat.xml',
        'views/views.xml',
        'views/server_actions.xml',
        'wizard/account_move_merge_wizard_view.xml',
        'report/report.xml',
        'report/account_move_merge_report.xml',
    ],
    "images": ["static/description/icon.png"],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    
    }
