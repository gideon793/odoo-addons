# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class rfq(models.Model):
    _name = 'sankerinvoicing.rfq'
    _rec_name = 'rfqnumber'
    rfqnumber = fields.Char('Reference Number', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: self._get_next_rfq())
    orderdate = fields.Date('Order Date', default=datetime.date.today())
    vendor = fields.Many2one('res.partner', string='Vendor', required=True)
    orderlines = fields.One2many('sankerinvoicing.rfqlines', 'rfq')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)

    @api.model
    def _get_next_rfq(self):
        sequence = self.env['ir.sequence'].search([('code', '=', 'sanker_rfq_order')])
        next = sequence.get_next_char(sequence.number_next_actual)
        return next

    @api.model
    def create(self, vals):
        vals['rfqnumber'] = self.env['ir.sequence'].next_by_code('sanker_rfq_order')
        res = super(rfq, self).create(vals)
        return res



class rfqlines(models.Model):
    _name = 'sankerinvoicing.rfqlines'
    rfq = fields.Many2one('sankerinvoicing.rfq')
    vendor = fields.Many2one('res.partner')
    product = fields.Many2one('product.product')
    notes = fields.Char('Notes')
    qty = fields.Integer(string='Product Quantity')
    orderdate = fields.Date('Order Date')
