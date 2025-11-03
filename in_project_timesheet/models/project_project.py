from odoo import models, fields, api, _
from odoo.addons.mail.models.mail_thread import MailThread
from odoo.addons.mail.models.mail_activity_mixin import MailActivityMixin

class ProjectTask(models.Model):
    _inherit = 'project.task'

    timer_start = fields.Datetime(string="Timer Start")
    is_timer_running = fields.Boolean(string="Is Timer Running", default=False)

    def action_timer_start(self):
        """Start the timer for the task"""
        for task in self:
            if not task.is_timer_running:
                task.timer_start = fields.Datetime.now()
                task.is_timer_running = True
                print(f"🔵 START TIMER: Task {task.name} at {task.timer_start}")
            else:
                print(f"⚠ Timer already running for task {task.name}")

    def action_timer_stop(self):
        """Stop the timer and create a timesheet entry"""
        for task in self:
            if task.is_timer_running and task.timer_start:
                total_seconds = (fields.Datetime.now() - task.timer_start).total_seconds()

                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                seconds = int(total_seconds % 60)
                time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                time_spent_hours = total_seconds / 3600.0

                if time_spent_hours > 0:
                    vals = {
                        'name': f"Work on {task.name} ({time_formatted})",
                        'unit_amount': time_spent_hours,
                        'task_id': task.id,
                        'project_id': task.project_id.id,
                        'employee_id': self.env.user.employee_id.id,
                    }
                    timesheet = self.env['account.analytic.line'].create(vals)
                    print(f"✅ Timesheet Created: {timesheet.name} ({time_spent_hours}h)")
                else:
                    print("⚠ Time spent is too small, no timesheet created.")

                task.is_timer_running = False
                task.timer_start = False
                print(f"🟥 STOP TIMER: Task {task.name} reset")
            else:
                print(f"⚠ Timer not running for task {task.name}")