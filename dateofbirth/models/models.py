# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,date
from dateutil.relativedelta import relativedelta


class dateofbirth(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    dob = fields.Date('Date of Birth')
    agecal = fields.Integer(string='Age')

    
    @api.onchange('dob')
    def _age(self):
        for record in self:
            if record.dob:
                dt=str(record.dob)
                d1=datetime.strptime(dt, "%Y-%m-%d").date()
                d2=date.today()
                record.agecal = relativedelta(d2, d1).years