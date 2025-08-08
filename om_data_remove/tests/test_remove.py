from odoo.tests.common import TransactionCase


class TestDataRemove(TransactionCase):
    def test_remove_sales(self):
        config = self.env['res.config.settings'].create({})
        self.assertTrue(config.remove_sales())
