from odoo.tests.common import TransactionCase


class TestAccountAccountant(TransactionCase):
    def test_invoice_payment_state(self):
        move = self.env['account.move']
        self.assertEqual(move._get_invoice_in_payment_state(), 'in_payment')
