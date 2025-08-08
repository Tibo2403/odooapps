from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import ValidationError


class TestFiscalYear(TransactionCase):
    def test_overlap_prevention(self):
        self.env['account.fiscal.year'].create({
            'name': 'FY1',
            'date_from': fields.Date.from_string('2023-01-01'),
            'date_to': fields.Date.from_string('2023-12-31'),
        })
        with self.assertRaises(ValidationError):
            self.env['account.fiscal.year'].create({
                'name': 'FY2',
                'date_from': fields.Date.from_string('2023-06-01'),
                'date_to': fields.Date.from_string('2023-12-31'),
            })
