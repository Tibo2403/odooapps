from odoo.tests.common import TransactionCase


class TestAccountFollowup(TransactionCase):
    def test_followup_line_sequence(self):
        followup = self.env['followup.followup'].create({})
        line1 = self.env['followup.line'].create({
            'name': 'Step1',
            'followup_id': followup.id,
            'delay': 10,
        })
        line2 = self.env['followup.line'].create({
            'name': 'Step2',
            'followup_id': followup.id,
            'delay': 20,
        })
        self.assertEqual(line1.sequence, 1)
        self.assertEqual(line2.sequence, 2)
