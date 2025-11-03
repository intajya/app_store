{
    'name': "Project Timer Enhancements",
    'version': '18.0.1.0.0',
    'summary': "Enhance project and timesheet management with integrated task timers, automatic timesheet logging.",
    'description': """
This module extends Odoo's Project and Timesheet applications by adding powerful time-tracking .
It allows users to start and stop timers directly from project tasks or timesheet lines, automatically creating analytic entries based on actual worked hours.
Additionally.
Key Features
-------------
- Task Timer Integration
  • Start and stop timers on project tasks.
  • Automatically record time spent in timesheets.
  • Calculate real working hours in account.analytic.line.

- Timesheet Enhancements
  • Start/Stop timer buttons directly inside the timesheet view.
  • Auto-update unit_amount based on recorded time.

Technical Highlights
--------------------
- Extends: project.task, account.analytic.line
- Adds dynamic timer management using datetime computation.
- Integrates seamlessly with CRM, HR Timesheet, and Project apps.

Dependencies
------------
- base, account, project, hr_timesheet
""",
    'author': "Intajya ",
    'category': 'Project/Time Tracking',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'project', 'hr_timesheet'],
    'data': [
        'views/project_project.xml',
        'views/timesheet_view.xml',
    ],
    "images": [
        "static/description/icon.png",
        "static/description/icon2.png",
               ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
