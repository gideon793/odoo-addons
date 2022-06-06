# -*- coding: utf-8 -*-

from odoo import models, fields, api


class monthlyacct(models.Model):
    _name = 'sankeremployee.monthly'
    _order = 'sequences, id'
    _rec_name = 'employee'
    employee = fields.Many2one('sankeremployee.sankeremployee', string='Employee name')
    designation = fields.Char(related='employee.designation', store=True, string='Designation')
    basic = fields.Float(string='Basic Pay')
    allowance = fields.Float(string='100% Fitment Allowance')
    grossdue = fields.Float(string='Gross Amount Due', compute="_gross", store=True)
    epfc = fields.Float(string='EPF contribution', compute="_epfc", store=True)
    professionaltax = fields.Float(string='Professional Tax')
    tds= fields.Float('Tax Deductable at Source')
    deduction = fields.Float(string='Total Deduction', compute="_deduct", store=True)
    netpayable = fields.Float(string='Net Amount Payable', compute="_net", store=True)
    salaries = fields.Many2one('sankeremployee.salaries', ondelete='cascade')
    days = fields.Integer('No. of days worked during the month')
    leave = fields.Integer('No. of days on leave during the month')
    worked = fields.Integer(string='No. of days for which salary is due')
    special = fields.Float(string='Special Duty Allowance')
    workingday = fields.Date(string='Last Working Day of the Month')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    month = fields.Char('Salary Month')
    sequences = fields.Integer(string='Sequence', required=True, copy=False, default='000')
    ddrspaid = fields.Float('Payment from DDRS')
    actualdue = fields.Float('Payment from Transaction Account', compute="_actual")
    
    @api.depends('basic')
    def _epfc(self):
        for record in self:
            if record.basic >= 15000:
                record.epfc = 1800
            else:
                record.epfc = round(record.basic * 0.12)

    @api.depends('basic', 'epfc','professionaltax','tds')
    def _deduct(self):
        for record in self:
            record.deduction = record.epfc + record.professionaltax + record.tds

    @api.depends('basic','allowance','special')
    def _gross(self):
        for record in self:
            record.grossdue = record.basic + record.allowance + record.special

    @api.depends('grossdue','epfc','professionaltax','tds')
    def _net(self):
        for record in self:
            record.netpayable = record.grossdue - record.epfc - record.professionaltax - record.tds

    @api.model
    def create(self, vals):
        if vals.get('sequences', 'New') == '000':
            vals['sequences'] = self.env['ir.sequence'].next_by_code('sankeremployee.monthly') or 'New'
        result = super(monthlyacct, self).create(vals)
        return result


    @api.depends('netpayable','ddrspaid')
    def _actual(self):
        for record in self:
            record.actualdue = record.netpayable - record.ddrspaid
