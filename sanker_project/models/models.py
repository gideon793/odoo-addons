
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from num2words import num2words


class project(models.Model):
    _name = 'sankerproject.project'
    name = fields.Char('Name of Project')

class projectdeals(models.Model):
    _name = 'sankerproject.projectdeals'
    _rec_name='project'
    project = fields.Many2one('sankerproject.project')
    outstanding = fields.Float('Outstanding Balance')
    transactions = fields.One2many('sankerproject.transactions', 'link')

    @api.onchange('transactions')
    def update_total(self):
        for record in self:
            if record.transactions:
                record.outstanding = 0
                vals = record.transactions
                for val in vals:
                    record.outstanding = record.outstanding + val.amount - val.paid


class transactions(models.Model):
    _name = 'sankerproject.transactions'
    project = fields.Many2one('sankerproject.project')
    link = fields.Many2one('sankerproject.projectdeals')
    date = fields.Date('Date of Transaction', default=date.today())
    amount = fields.Float('Total Amount Due', default=0)
    paid = fields.Float('Total Amount Paid', default=0)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    paid_text = fields.Char(compute='_amountwords')

    def _amountwords(self):
        for record in self:
            record.paid_text = num2words(record.paid, lang='en_IN')

