# -*- coding: utf-8 -*-

from odoo import models, fields, api

class updateinvoice(models.Model):
    _inherit = 'account.invoice'
    isip = fields.Boolean(string='IP patient')
    medicinebill = fields.Boolean(string='Is this a medicine bill')


