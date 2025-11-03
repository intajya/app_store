from odoo import models, fields

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    timer_start = fields.Datetime(string="Timer Start")
    is_timer_running = fields.Boolean(string="Is Timer Running", default=False)

    def action_timer_start(self):
        for line in self:
            if not line.is_timer_running:
                line.timer_start = fields.Datetime.now()
                line.is_timer_running = True
                print("=== TIMER STARTED ===")
                print(f"Record ID: {line.id}")
                print(f"Name: {line.name}")
                print(f"Start Time: {line.timer_start}")
                print(f"Current Unit Amount: {line.unit_amount}")
                print("=====================")

    def action_timer_stop(self):
        for line in self:
            if line.is_timer_running and line.timer_start:
                delta = fields.Datetime.now() - line.timer_start
                hours = delta.total_seconds() / 3600
                line.unit_amount += hours
                print("=== TIMER STOPPED ===")
                print(f"Record ID: {line.id}")
                print(f"Name: {line.name}")
                print(f"Start Time: {line.timer_start}")
                print(f"Stop Time: {fields.Datetime.now()}")
                print(f"Hours Added: {hours:.2f}")
                print(f"Updated Unit Amount: {line.unit_amount}")
                print("=====================")
                line.timer_start = False
                line.is_timer_running = False
