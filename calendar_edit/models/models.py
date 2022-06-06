# -*- coding: utf-8 -*-

from odoo import models, fields, api

class calendar_edit(models.Model):
    _inherit = 'calendar.event'
    patient = fields.Many2one('res.partner', string='Patient Name')

