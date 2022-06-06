# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class appointment(models.Model):
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    apptdate = fields.Datetime('Appointment Date')
    allday=fields.Boolean('All day?', default=False)
    registration = fields.Char(related='partner_id.registration',store=True)
    mobile=fields.Char(related='partner_id.mobile',store=True)

 		


