# -*- coding: utf-8 -*-

from odoo import models, fields
from num2words import num2words


class ipbill(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order'
    registration = fields.Char(related='partner_id.registration')
    admdate = fields.Date(string='Date of Admission')
    discdate = fields.Date(string='Date of Discharge')
    isip = fields.Boolean(string='IP patient')
    medicinebill = fields.Boolean(string='Is this a medicine bill')
    accomodation = fields.Char(string='Accomodation Type', size=12)
    periodbill = fields.Char(string='Period of Bill', size =40)
    ipregno = fields.Char(related='partner_id.ipregno')
    text_amount = fields.Char(compute='_amountwords',string='Amount in words')
    amount_round = fields.Monetary(compute='_amountround', string='Rounded off')
    amount_diff=fields.Monetary(compute='_amountdiff',string='Amount rounded off')    
    remarks = fields.Char(string='Remarks', size =100)
    
    def _amountwords(self):
        for record in self:
            record.text_amount= num2words(record.amount_round, lang='en_IN', to='currency', currency='INR')
    
    def _amountround(self):
        for record in self:
            record.amount_round = round(record.amount_total)

    def _amountdiff(self):
        for record in self:
            record.amount_diff = record.amount_total - record.amount_round

