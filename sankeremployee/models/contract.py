# -*- coding: utf-8 -*-

from odoo import models, fields, api

class contractemployee(models.Model):
    _name = 'sankeremployee.contractemployee'
    name = fields.Char('Employee Name')
    employmentno = fields.Char('Employment Number')
    age = fields.Integer('Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string='Gender')
    designation = fields.Char('Designation')
    grossdue = fields.Float('Basic Pay')
    annualpay = fields.Float(compute='_annualpay', string='Computed Annual Pay')
    acctno = fields.Char('SBI Account Number')
    branch = fields.Char('SBI Branch Code')

    def _annualpay(self):
        for record in self:
            record.annualpay = record.grossdue * 12
