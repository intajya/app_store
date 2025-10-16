from odoo import models, fields


class AccountMoveMergeWizardLine(models.TransientModel):
    _name = 'account.move.merge.wizard.line'
    _description = 'Account Move Merge Wizard Line'

    wizard_id = fields.Many2one('account.move.merge.wizard')
    account_id = fields.Many2one('account.account', string='Account')
    product_id = fields.Many2one('product.product', string='Product')
    name = fields.Char('Label')
    quantity = fields.Float(string='Total Quantity')
    price_unit = fields.Float(string='Price Unit')
    debit = fields.Monetary('Debit')
    credit = fields.Monetary('Credit')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    line_total = fields.Monetary(string='Total')
    payment_method_type = fields.Selection([
        ('cash', 'Cash'),
        ('wallet', 'Wallet'),
        ('on line', 'On Line')
    ], string="Payment Type")
