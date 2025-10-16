from collections import defaultdict
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMoveMergeWizard(models.TransientModel):
    _name = 'account.move.merge.wizard'
    _description = 'Merge Account Moves Wizard'

    invoice_ids = fields.Many2many('account.move', string='Invoices')
    merged_line_ids = fields.One2many('account.move.merge.wizard.line', 'wizard_id', string="Merged Lines")
    partner_id = fields.Many2one('res.partner', string="Customer", readonly=True)
    report_number = fields.Char(string="Report Number", readonly=True, copy=False)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        invoices = self.env['account.move'].browse(active_ids)

        res['invoice_ids'] = [(6, 0, active_ids)]

        partners = invoices.mapped('partner_id')
        if len(partners) > 1:
            raise UserError(_("You can only merge invoices for the same customer."))
        elif partners:
            res['partner_id'] = partners[0].id

        # Merge lines
        line_data = defaultdict(lambda: {
            'product_id': False,
            'quantity': 0.0,
            'price_unit': 0.0,
            'debit': 0.0,
            'credit': 0.0,
            'name': '',
            'account_id': False,
            'line_total': 0.0,
        })

        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                key = line.product_id.id
                if not key:
                    continue

                taxes = line.tax_ids.compute_all(
                    line.price_unit,
                    quantity=line.quantity,
                    currency=invoice.currency_id,
                    product=line.product_id,
                    partner=invoice.partner_id,
                )
                line_total = taxes['total_included']

                data = line_data[key]
                data['product_id'] = line.product_id.id
                data['quantity'] += line.quantity
                data['price_unit'] = line.price_unit
                data['name'] = line.name
                data['account_id'] = line.account_id.id
                data['line_total'] += line_total

        merged_lines = []
        total_quantity = 0.0
        total_price_total = 0.0

        for item in line_data.values():
            line_total = item['line_total']
            total_quantity += item['quantity']
            total_price_total += line_total

            merged_lines.append((0, 0, {
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'price_unit': item['price_unit'],
                'debit': item['debit'],
                'credit': item['credit'],
                'name': item['name'],
                'account_id': item['account_id'],
                'line_total': line_total,
            }))

        merged_lines.append((0, 0, {
            'product_id': False,
            'quantity': total_quantity,
            'price_unit': 0.0,
            'debit': 0.0,
            'credit': 0.0,
            'name': f'Total ({len(line_data)} Products)',
            'account_id': False,
            'line_total': total_price_total,
        }))

        payment_method_type_totals = defaultdict(float)
        for invoice in invoices:
            payment_method_type = invoice.payment_method_type
            if payment_method_type:
                payment_method_type_totals[payment_method_type] += invoice.amount_total

        for pay_type, total in payment_method_type_totals.items():
            merged_lines.append((0, 0, {
                'product_id': False,
                'quantity': 0.0,
                'price_unit': 0.0,
                'debit': 0.0,
                'credit': 0.0,
                'name': f'Total for {pay_type.capitalize()}',
                'account_id': False,
                'payment_method_type': pay_type,
                'line_total': total,
            }))

        res['merged_line_ids'] = merged_lines
        return res

    def print_report(self):
        for wizard in self:
            if not wizard.report_number:
                wizard.report_number = self.env['ir.sequence'].next_by_code('account.move.merge.report') or '/'
        return self.env.ref('in_custom_journal_entries.action_report_account_move_merge').report_action(self)
