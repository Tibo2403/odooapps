from odoo.tests.common import TransactionCase
from odoo import fields


class TestAccountAsset(TransactionCase):
    def test_asset_depreciation_board(self):
        account_asset = self.env['account.account'].create({
            'name': 'Asset Account',
            'code': 'ASSET1',
            'account_type': 'asset_non_current',
        })
        account_depr = self.env['account.account'].create({
            'name': 'Depreciation Account',
            'code': 'DEPR1',
            'account_type': 'asset_non_current',
        })
        account_expense = self.env['account.account'].create({
            'name': 'Expense Account',
            'code': 'EXP1',
            'account_type': 'expense',
        })
        journal = self.env['account.journal'].create({
            'name': 'Misc',
            'code': 'MISC',
            'type': 'general',
        })
        category = self.env['account.asset.category'].create({
            'name': 'Test Category',
            'account_asset_id': account_asset.id,
            'account_depreciation_id': account_depr.id,
            'account_depreciation_expense_id': account_expense.id,
            'journal_id': journal.id,
            'method_number': 5,
            'method_period': 12,
        })
        asset = self.env['account.asset.asset'].create({
            'name': 'Test Asset',
            'category_id': category.id,
            'value': 1000.0,
            'date': fields.Date.today(),
        })
        asset.compute_depreciation_board()
        self.assertGreater(len(asset.depreciation_line_ids), 0)
