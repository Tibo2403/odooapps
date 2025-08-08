from odoo.tests.common import TransactionCase
from odoo import fields


class TestAccountingPdfReports(TransactionCase):
    def test_accounting_report_action(self):
        account = self.env['account.account'].create({
            'name': 'Test Account',
            'code': 'TST1',
            'account_type': 'asset_current',
        })
        report = self.env['account.financial.report'].create({
            'name': 'Report',
            'type': 'accounts',
            'account_ids': [(6, 0, [account.id])],
        })
        journal = self.env['account.journal'].create({
            'name': 'Misc',
            'code': 'MISC',
            'type': 'general',
        })
        wizard = self.env['accounting.report'].create({
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today(),
            'target_move': 'posted',
            'journal_ids': [(6, 0, [journal.id])],
            'account_report_id': report.id,
        })
        action = wizard.check_report()
        self.assertTrue(action)
