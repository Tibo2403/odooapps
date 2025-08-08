from odoo.tests.common import TransactionCase


class TestPayrollAccount(TransactionCase):
    def test_default_journal(self):
        slip = self.env['hr.payslip'].new({})
        self.assertTrue(slip.journal_id)
