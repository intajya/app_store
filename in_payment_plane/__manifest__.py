{
    'name': "Sales Payment Plan & Installments",
    'version': '18.0.1.0.0',
    'summary': "Manage sales payment plans with discounts, down payments, and automatic installment invoicing.",
    'description': """
This module enhances Odoo's Sales and Accounting applications by introducing flexible payment plan management.
It allows users to define discount rates, down payment percentages, and periodic installment frequencies directly from the Sale Order form.

Key Features
-------------
- Payment Plan Management
  • Define customizable payment plans (monthly, quarterly, semi-annual).
  • Add discounts, down payments, and annual payments per sale order.
  • Automatically calculate installment schedules and payment dates.

- Installment Automation
  • Automatically generate installment lines within the sale order.
  • Create invoices for each installment with a single click.
  • View and track all related installment invoices via smart buttons.

Technical Highlights
--------------------
- Extends: sale.order, account.move
- Adds new models: payment.plane, sale.order.installment.line
- Uses computed fields for financial breakdown and date generation.
- Seamlessly integrates with Odoo Accounting and Sales modules.

Dependencies
------------
- base
- sale_management
- account
""",
    'author': "Intajya",
    'category': 'Sales/Payment',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_plane_view.xml',
        'views/sale_order_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
