# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _
from num2words import num2words


class contractmonthlyacct(models.Model):
    _name = 'sankeremployee.contractmonthly'
    _order = 'sequences, id'
    employee = fields.Many2one('sankeremployee.contractemployee', string='Employee name')
    designation = fields.Char(related='employee.designation', store=True, string='Designation')
    particulars = fields.Char(string='Particulars', required=True)
    grossdue = fields.Float(string='Gross Amount Due')
    salaries = fields.Many2one('sankeremployee.contractsalaries', ondelete='cascade')
    days = fields.Integer('No. of days worked during the month')
    leave = fields.Integer('No. of days on leave during the month')
    worked = fields.Integer(string='No. of days for which salary is due')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    receipt_no = fields.Char(string='Receipt  No')
    text_amount = fields.Char(compute='_amountwords', string='Amount in words')
    workingday = fields.Date(string='Last Working Day of the Month')
    month = fields.Char('Salary Month')
    sequences = fields.Integer(string='Sequence', required=True, copy=False, default='000')

    @api.model
    def create(self, vals):
        if vals.get('sequences', 'New') == '000':
            vals['sequences'] = self.env['ir.sequence'].next_by_code('sankeremployee.monthly') or 'New'
        result = super(contractmonthlyacct, self).create(vals)
        return result

    def _amountwords(self):
        for record in self:
            record.text_amount = num2words(record.grossdue, lang='en_IN')


