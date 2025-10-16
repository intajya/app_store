from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_method_type = fields.Selection([
        ('cash', 'Cash'),
        ('wallet', 'Wallet'),
        ('on line', 'On Line')
    ], string="Payment Type")
    expected_currency_rate = fields.Float(string="Expected Currency Rate")


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    exclude_bank_lines = fields.Boolean(
        string="Exclude Bank Lines",
        help="Exclude this journal entry line from being included in tax or audit reports."
    )

