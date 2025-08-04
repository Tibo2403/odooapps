import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class HrPayrollStructure(models.Model):
    _name = 'hr.payroll.structure'
    _description = 'Salary Structure'

    @api.model
    def _get_parent(self):
        return self.env.ref('om_hr_payroll.structure_base', False)

    name = fields.Char(required=True)
    code = fields.Char(string='Reference', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    note = fields.Text(string='Description')
    parent_id = fields.Many2one('hr.payroll.structure', string='Parent', default=_get_parent)
    children_ids = fields.One2many('hr.payroll.structure', 'parent_id', string='Children', copy=True)
    rule_ids = fields.Many2many('hr.salary.rule', 'hr_structure_salary_rule_rel', 'struct_id', 'rule_id', string='Salary Rules')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create a recursive salary structure.'))

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, code=_("%s (copy)") % (self.code))
        return super(HrPayrollStructure, self).copy(default)

    def get_all_rules(self):
        all_rules = []
        for struct in self:
            all_rules += struct.rule_ids._recursive_search_of_rules()
        return all_rules

    def _get_parent_structure(self):
        parent = self.mapped('parent_id')
        if parent:
            parent = parent._get_parent_structure()
        return parent + self


class HrContributionRegister(models.Model):
    _name = 'hr.contribution.register'
    _description = 'Contribution Register'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', string='Partner')
    name = fields.Char(required=True)
    register_line_ids = fields.One2many('hr.payslip.line', 'register_id', string='Register Line', readonly=True)
    note = fields.Text(string='Description')


class HrSalaryRuleCategory(models.Model):
    _name = 'hr.salary.rule.category'
    _description = 'Salary Rule Category'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    parent_id = fields.Many2one('hr.salary.rule.category', string='Parent',
        help="Linking a salary category to its parent is used only for the reporting purpose.")
    children_ids = fields.One2many('hr.salary.rule.category', 'parent_id', string='Children')
    note = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive hierarchy of Salary Rule Category.'))


class HrSalaryRule(models.Model):
    _name = 'hr.salary.rule'
    _order = 'sequence, id'
    _description = 'Salary Rule'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, help="The code of salary rules can be used as reference in computation of other rules. It is case sensitive.")
    sequence = fields.Integer(required=True, index=True, default=5, help='Use to arrange calculation sequence')
    quantity = fields.Char(default='1.0', help="Used in computation for percentage and fixed amount.")
    category_id = fields.Many2one('hr.salary.rule.category', string='Category', required=True)
    active = fields.Boolean(default=True, help="If false, hides the salary rule without removing it.")
    appears_on_payslip = fields.Boolean(string='Appears on Payslip', default=True)
    parent_rule_id = fields.Many2one('hr.salary.rule', string='Parent Salary Rule', index=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    condition_select = fields.Selection([
        ('none', 'Always True'),
        ('range', 'Range'),
        ('python', 'Python Expression')
    ], string="Condition Based on", default='none', required=True)
    condition_range = fields.Char(string='Range Based on', default='contract.wage')
    condition_python = fields.Text(string='Python Condition', required=True, default='''
        result = rules.NET > categories.NET * 0.10''')
    condition_range_min = fields.Float(string='Minimum Range')
    condition_range_max = fields.Float(string='Maximum Range')
    amount_select = fields.Selection([
        ('percentage', 'Percentage (%)'),
        ('fix', 'Fixed Amount'),
        ('code', 'Python Code'),
    ], string='Amount Type', index=True, required=True, default='fix')
    amount_fix = fields.Float(string='Fixed Amount')
    amount_percentage = fields.Float(string='Percentage (%)')
    amount_python_compute = fields.Text(string='Python Code', default='''
        result = contract.wage * 0.10''')
    amount_percentage_base = fields.Char(string='Percentage based on')
    child_ids = fields.One2many('hr.salary.rule', 'parent_rule_id', string='Child Salary Rule', copy=True)
    register_id = fields.Many2one('hr.contribution.register', string='Contribution Register')
    input_ids = fields.One2many('hr.rule.input', 'input_id', string='Inputs', copy=True)
    note = fields.Text(string='Description')

    @api.constrains('parent_rule_id')
    def _check_parent_rule_id(self):
        if not self._check_recursion(parent='parent_rule_id'):
            raise ValidationError(_('Error! You cannot create recursive hierarchy of Salary Rules.'))

    def _recursive_search_of_rules(self):
        children_rules = []
        for rule in self.filtered(lambda rule: rule.child_ids):
            children_rules += rule.child_ids._recursive_search_of_rules()
        return [(rule.id, rule.sequence) for rule in self] + children_rules

    def _compute_rule(self, localdict):
        self.ensure_one()
        if self.amount_select == 'fix':
            try:
                return self.amount_fix, float(safe_eval(self.quantity, localdict)), 100.0
            except (ValueError, TypeError, NameError, SyntaxError) as error:
                _logger.exception("Wrong quantity defined for salary rule %s (%s): %s", self.name, self.code, error)
                raise UserError(_('Wrong quantity defined for salary rule %s (%s).') % (self.name, self.code))
        elif self.amount_select == 'percentage':
            try:
                return (
                    float(safe_eval(self.amount_percentage_base, localdict)),
                    float(safe_eval(self.quantity, localdict)),
                    self.amount_percentage
                )
            except (ValueError, TypeError, NameError, SyntaxError) as error:
                _logger.exception("Wrong percentage base or quantity for salary rule %s (%s): %s", self.name, self.code, error)
                raise UserError(_('Wrong percentage base or quantity defined for salary rule %s (%s).') % (self.name, self.code))
        else:
            try:
                safe_eval(self.amount_python_compute, localdict, mode='exec', nocopy=True)
                result = localdict['result']
                if not isinstance(result, float):
                    raise UserError(_('Wrong python code result type for salary rule %s (%s): expected float, got %s') % (self.name, self.code, type(result).__name__))
                return (
                    float(result),
                    localdict.get('result_qty', 1.0),
                    localdict.get('result_rate', 100.0),
                )
            except Exception as ex:
                _logger.exception("Wrong python code defined for salary rule %s (%s): %s", self.name, self.code, ex)
                raise UserError(_("Wrong python code defined for salary rule %s (%s).\nHere is the error received:\n%s") % (self.name, self.code, repr(ex)))

    def _satisfy_condition(self, localdict):
        self.ensure_one()
        if self.condition_select == 'none':
            return True
        elif self.condition_select == 'range':
            try:
                result = safe_eval(self.condition_range, localdict)
                return self.condition_range_min <= result <= self.condition_range_max or False
            except (ValueError, TypeError, NameError, SyntaxError) as error:
                _logger.exception("Wrong range condition defined for salary rule %s (%s): %s", self.name, self.code, error)
                raise UserError(_('Wrong range condition defined for salary rule %s (%s).') % (self.name, self.code))
        else:
            try:
                safe_eval(self.condition_python, localdict, mode='exec', nocopy=True)
                return localdict.get('result', False)
            except Exception as ex:
                _logger.exception("Wrong python condition defined for salary rule %s (%s): %s", self.name, self.code, ex)
                raise UserError(_("Wrong python condition defined for salary rule %s (%s).\nHere is the error received:\n%s") % (self.name, self.code, repr(ex)))


class HrRuleInput(models.Model):
    _name = 'hr.rule.input'
    _description = 'Salary Rule Input'

    name = fields.Char(string='Description', required=True)
    code = fields.Char(required=True, help="The code that can be used in the salary rules")
    input_id = fields.Many2one('hr.salary.rule', string='Salary Rule Input', required=True)
