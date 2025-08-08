from odoo.tests.common import TransactionCase
from odoo import fields
from dateutil.relativedelta import relativedelta


class TestRecurringPayments(TransactionCase):
    def test_recurring_payment_lines(self):
        partner = self.env['res.partner'].create({'name': 'Test'})
        journal = self.env['account.journal'].create({
            'name': 'Bank',
            'code': 'BNK1',
            'type': 'bank',
        })
        template = self.env['account.recurring.template'].create({
            'name': 'Template',
            'journal_id': journal.id,
            'recurring_period': 'months',
            'journal_state': 'draft',
            'recurring_interval': 1,
            'state': 'done',
        })
        payment = self.env['recurring.payment'].create({
            'partner_id': partner.id,
            'amount': 100,
            'journal_id': journal.id,
            'template_id': template.id,
            'date_begin': fields.Date.today(),
            'date_end': fields.Date.today() + relativedelta(days=1),
        })
        payment.action_done()
        self.assertEqual(len(payment.line_ids), 1)
