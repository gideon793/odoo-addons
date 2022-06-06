# -*- coding: utf-8 -*-

from odoo import models, fields, api

class diagnosis(models.Model):
    _name = 'diagnosis.diagnosis'

    name = fields.Char(string='Diagnosis')
    code = fields.Char(strin='Code')
