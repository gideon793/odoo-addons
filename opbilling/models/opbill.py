# -*- coding: utf-8 -*-

from odoo import models, fields

class ipbill(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order'
    registration = fields.Char(related='partner_id.registration',store=True)
    isop = fields.Boolean(string='Is this an OP patient')
    consultfee = fields.Integer(string='Consultation Fee')
