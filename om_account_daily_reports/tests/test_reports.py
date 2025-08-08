from odoo.tests.common import TransactionCase
from odoo import fields


class TestDailyReports(TransactionCase):
    def test_cashbook_report(self):
        account = self.env['account.account'].create({
            'name': 'Cash',
            'code': 'CASH1',
            'account_type': 'asset_cash',
        })
        journal = self.env['account.journal'].create({
            'name': 'Cash',
            'code': 'CASH',
            'type': 'cash',
            'default_account_id': account.id,
        })
        wizard = self.env['account.cashbook.report'].create({
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today(),
            'target_move': 'posted',
            'journal_ids': [(6, 0, [journal.id])],
            'account_ids': [(6, 0, [account.id])],
            'display_account': 'movement',
            'sortby': 'sort_date',
        })
        action = wizard.check_report()
        self.assertTrue(action)
