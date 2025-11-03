from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    installment_sale_id = fields.Many2one('sale.order', string="Installment Sale Order")
