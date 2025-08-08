from odoo.tests.common import TransactionCase
from odoo import fields


class TestPayslipPrepareData(TransactionCase):
    def test_prepare_payslip_data_defaults(self):
        today = fields.Date.today()
        res = self.env['hr.payslip'].prepare_payslip_data(today, today)
        self.assertIn('value', res)
        value = res['value']
        self.assertEqual(value['line_ids'], [])
        self.assertEqual(value['input_line_ids'], [])
        self.assertEqual(value['worked_days_line_ids'], [])
        self.assertEqual(value['name'], '')
        self.assertFalse(value['contract_id'])
        self.assertFalse(value['struct_id'])

