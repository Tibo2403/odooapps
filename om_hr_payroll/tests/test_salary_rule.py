from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestSalaryRule(TransactionCase):
    def test_compute_rule_invalid_result_type(self):
        category = self.env['hr.salary.rule.category'].create({
            'name': 'Basic',
            'code': 'BASIC'
        })
        rule = self.env['hr.salary.rule'].create({
            'name': 'Invalid Result Rule',
            'code': 'INV',
            'sequence': 1,
            'category_id': category.id,
            'amount_select': 'code',
            'amount_python_compute': 'result = "abc"',
        })
        with self.assertRaises(UserError):
            rule._compute_rule({})
