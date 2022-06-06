# -*- coding: utf-8 -*-

from odoo import models, fields, api

class my_sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    @api.multi
    def _prepare_invoice(self):
        invoice_vals=super(my_sale_order, self)._prepare_invoice()
        invoice_vals['isip']=self.isip
        invoice_vals['medicinebill']=self.medicinebill
        return invoice_vals
        
