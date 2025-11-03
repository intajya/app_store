from odoo import api, fields, models

class PaymentPlan(models.Model):
    _name = "payment.plane"
    _description = "Payment Plan"

    name = fields.Char(string='Name', required=True)
    discount = fields.Float(string="Discount %", default=0.0)
    down_payment_percentage = fields.Float(string="Down Payment %")
    annual_payment_percentage = fields.Float(string="Annual Payment %")
    payment_start_date = fields.Date(string="Payment Start Date", default=fields.Date.context_today)
    payment_duration = fields.Integer(string="Payment Duration (Years)", default=1)
    payment_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annually', 'Semi-Annually')
    ], string="Payment Frequency", default='monthly')

    price_after_discount = fields.Float(string="Price After Discount",
                                        compute='_compute_price_after_discount', store=True)
    down_payment = fields.Float(string="Down Payment Amount",
                                compute="_compute_down_payment", store=True)
    total_annual_payment_amount = fields.Float(string="Total Annual Payments",
                                               compute="_compute_annual_payment", store=True)
    amount_to_be_installed = fields.Float(string="Amount for Periodic Installments",
                                          compute="_compute_final_amount", store=True)
    no_of_installments = fields.Integer(string="Number of Periodic Installments",
                                        compute='_compute_installments', store=True)
    amount_per_installment = fields.Float(string="Amount Per Periodic Installment",
                                          compute='_compute_installments', store=True)

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    installment_line_ids = fields.One2many(
        'sale.order.installment.line',
        'payment_plan_id',
        string='Installment Lines'
    )

    @api.depends('discount', 'sale_order_id.amount_total')
    def _compute_price_after_discount(self):
        for plan in self:
            total = plan.sale_order_id.amount_total or 0.0
            plan.price_after_discount = total * (1 - (plan.discount / 100))

    @api.depends('down_payment_percentage', 'price_after_discount')
    def _compute_down_payment(self):
        for plan in self:
            plan.down_payment = plan.price_after_discount * (plan.down_payment_percentage / 100)

    @api.depends('annual_payment_percentage', 'price_after_discount', 'payment_duration')
    def _compute_annual_payment(self):
        for plan in self:
            plan.total_annual_payment_amount = (
                plan.price_after_discount * (plan.annual_payment_percentage / 100) * plan.payment_duration
            )

    @api.depends('price_after_discount', 'down_payment', 'total_annual_payment_amount')
    def _compute_final_amount(self):
        for plan in self:
            plan.amount_to_be_installed = (
                plan.price_after_discount - plan.down_payment - plan.total_annual_payment_amount
            )

    @api.depends('payment_frequency', 'payment_duration', 'amount_to_be_installed')
    def _compute_installments(self):
        for plan in self:
            if plan.payment_frequency == 'monthly':
                plan.no_of_installments = plan.payment_duration * 12
            elif plan.payment_frequency == 'quarterly':
                plan.no_of_installments = plan.payment_duration * 4
            elif plan.payment_frequency == 'semi_annually':
                plan.no_of_installments = plan.payment_duration * 2
            else:
                plan.no_of_installments = 0

            plan.amount_per_installment = (
                plan.amount_to_be_installed / plan.no_of_installments
                if plan.no_of_installments > 0 else 0
            )


class SaleOrderInstallmentLine(models.Model):
    _name = 'sale.order.installment.line'
    _description = 'Sale Order Installment Line'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order", ondelete='cascade')
    payment_plan_id = fields.Many2one('payment.plane', string="Payment Plan", ondelete='cascade')
    installment_no = fields.Char(string="Installment No.")
    installment_date = fields.Date(string="Installment Date")
    amount = fields.Float(string="Installment Amount")
