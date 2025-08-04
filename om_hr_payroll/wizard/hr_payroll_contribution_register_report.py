from dateutil import relativedelta

from odoo import api, fields, models


class PayslipLinesContributionRegister(models.TransientModel):
    _name = 'payslip.lines.contribution.register'
    _description = 'Payslip Lines by Contribution Registers'

    date_from = fields.Date(
        string='Date From',
        required=True,
        default=lambda self: fields.Date.to_string(fields.Date.today().replace(day=1)),
    )
    date_to = fields.Date(
        string='Date To',
        required=True,
        default=lambda self: fields.Date.to_string(
            fields.Date.today() + relativedelta.relativedelta(months=+1, day=1, days=-1)
        ),
    )

    def print_report(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
             'ids': active_ids,
             'model': 'hr.contribution.register',
             'form': self.read()[0]
        }
        return self.env.ref('om_om_hr_payroll.action_contribution_register').report_action([], data=datas)
