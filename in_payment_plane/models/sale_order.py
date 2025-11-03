from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_plan_id = fields.Many2one('payment.plane', string="Payment Plan")
    installment_line_ids = fields.One2many('sale.order.installment.line', 'sale_order_id', string="Installments")
    installment_invoice_ids = fields.One2many(
        'account.move', 'installment_sale_id', string="Installment Invoices"
    )
    @api.onchange('payment_plan_id')
    def _onchange_payment_plan_id(self):
        for order in self:
            order.installment_line_ids = [(5, 0, 0)]
            plan = order.payment_plan_id
            if not plan:
                continue

            total_price = order.amount_total or 0.0

            price_after_discount = total_price * (1 - (plan.discount / 100))

            down_payment = price_after_discount * (plan.down_payment_percentage / 100)

            remaining_after_down = price_after_discount - down_payment

            annual_payment_per_year = remaining_after_down * (plan.annual_payment_percentage / 100)
            total_annual_payment = annual_payment_per_year * plan.payment_duration

            remaining_for_installments = remaining_after_down - total_annual_payment

            freq_map = {
                'monthly': 12,
                'quarterly': 4,
                'semi_annually': 2,
                'annually': 1,
            }
            periods_per_year = freq_map.get(plan.payment_frequency, 1)
            total_installments = plan.payment_duration * periods_per_year

            amount_per_installment = (
                remaining_for_installments / total_installments if total_installments > 0 else 0
            )

            start_date = fields.Date.today()
            step_months = {
                'monthly': 1,
                'quarterly': 3,
                'semi_annually': 6,
                'annually': 12,
            }.get(plan.payment_frequency, 1)

            installment_vals = []

            if down_payment > 0:
                installment_vals.append((0, 0, {
                    'installment_no': 0,
                    'installment_date': start_date,
                    'amount': down_payment,
                }))

            for year in range(plan.payment_duration):
                annual_date = start_date + relativedelta(years=year)
                installment_vals.append((0, 0, {
                    'installment_no': f"Y{year+1}",
                    'installment_date': annual_date,
                    'amount': annual_payment_per_year,
                }))

            for i in range(total_installments):
                due_date = start_date + relativedelta(months=i * step_months)
                installment_vals.append((0, 0, {
                    'installment_no': i + 1,
                    'installment_date': due_date,
                    'amount': amount_per_installment,
                }))

            order.installment_line_ids = installment_vals

    def action_create_installment_invoices(self):
        """Create customer invoices for each installment line."""
        account_move = self.env['account.move']
        created_invoices = self.env['account.move']

        for order in self:
            if not order.installment_line_ids:
                raise UserError(_("No installment lines found for this Sale Order."))

            for line in order.installment_line_ids:
                if line.amount <= 0:
                    continue

                invoice_vals = {
                    'move_type': 'out_invoice',  # Customer Invoice
                    'partner_id': order.partner_id.id,
                    'invoice_origin': order.name,
                    'invoice_date': line.installment_date,
                    'invoice_payment_term_id': False,
                    'installment_sale_id': order.id,
                    'invoice_line_ids': [(0, 0, {
                        'name': f"Installment {line.installment_no or ''}",
                        'quantity': 1,
                        'price_unit': line.amount,
                        'tax_ids': [(6, 0, order.order_line[0].tax_id.ids)] if order.order_line else False,
                        'product_id': order.order_line[0].product_id.id if order.order_line else False,
                        'account_id': order.order_line[0].product_id.property_account_income_id.id
                                      or order.order_line[0].product_id.categ_id.property_account_income_categ_id.id,
                    })],
                }

                new_invoice = account_move.create(invoice_vals)
                created_invoices |= new_invoice

        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(created_invoices) == 1:
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = created_invoices.id
        else:
            action['domain'] = [('id', 'in', created_invoices.ids)]
        return action

    def action_view_installment_invoices(self):
        """Smart button: open all invoices created from this Sale Order installments."""
        self.ensure_one()
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [('installment_sale_id', '=', self.id)]
        action['context'] = {'default_installment_sale_id': self.id}
        action['name'] = _('Installment Invoices')
        return action