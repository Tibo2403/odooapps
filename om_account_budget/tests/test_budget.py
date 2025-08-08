from odoo.tests.common import TransactionCase
from odoo import fields
from dateutil.relativedelta import relativedelta


class TestAccountBudget(TransactionCase):
    def test_budget_creation(self):
        account = self.env['account.account'].create({
            'name': 'Budget Account',
            'code': 'BUD01',
            'account_type': 'expense',
        })
        budget_post = self.env['account.budget.post'].create({
            'name': 'Post',
            'account_ids': [(6, 0, [account.id])],
        })
        analytic = self.env['account.analytic.account'].create({'name': 'Analytic'})
        budget = self.env['crossovered.budget'].create({
            'name': 'Budget',
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today() + relativedelta(months=1),
        })
        line = self.env['crossovered.budget.lines'].create({
            'crossovered_budget_id': budget.id,
            'date_from': budget.date_from,
            'date_to': budget.date_to,
            'analytic_account_id': analytic.id,
            'general_budget_id': budget_post.id,
            'planned_amount': 1000,
        })
        self.assertIn(line, budget.crossovered_budget_line)
