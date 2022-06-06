# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class certificates(models.Model):
    _name='opregistration.certificates'
    partner_id= fields.Many2one('res.partner', string='Patient name')
    _rec_name = 'partner_id'
    registration = fields.Char(related='partner_id.registration')
    gender = fields.Selection(related='partner_id.gender')
    diagnosis = fields.Char('Diagnosis')
    duration = fields.Char('Duration of Leave')
    date_from=fields.Date('Date From')
    date_to = fields.Date('Date To')
    date = fields.Date('Date', default = fields.Date.today ())
    doctor = fields.Selection([('ssyiem','Dr. S. Syiem'),('eddie','Dr. E. Mukhim'),('didak','Dr. D. Khonglah'),('gideon','Dr. G. Rynjah'),('rlaloo','Dr. R. Laloo'),('dkynjin','Dr. D. Kynjin')],string = 'Doctor')
    dob = fields.Date(related='partner_id.dob')
    agecal = fields.Integer(compute='_age',store=True, group_operator=False)
    period = fields.Char('Period of Leave')
    periodunit = fields.Selection([('days','Days'),('weeks','Weeks'),('months','Months')])

    @api.depends('dob','date')
    def _age(self):
        for record in self:
            if record.dob:
                dt=str(record.dob)
                d1=datetime.strptime(dt, "%Y-%m-%d").date()
                d2=record.date
                record.agecal = relativedelta(d2, d1).years


class certificates(models.Model):
    _name='opregistration.fitness'
    partner_id= fields.Many2one('res.partner', string='Patient name')
    _rec_name = 'partner_id'
    registration = fields.Char(related='partner_id.registration')
    gender = fields.Selection(related='partner_id.gender')
    diagnosis = fields.Char('Diagnosis')
    dob = fields.Date(related='partner_id.dob')
    agecal = fields.Integer(compute='_age',store=True, group_operator=False)
    date = fields.Date('Date', default = fields.Date.today ())
    doctor = fields.Selection([('ssyiem','Dr. S. Syiem'),('eddie','Dr. E. Mukhim'),('didak','Dr. D. Khonglah'),('gideon','Dr. G. Rynjah'),('rlaloo','Dr. R. Laloo'),('dkynjin','Dr. D. Kynjin')],string = 'Doctor')
    joining = fields.Date('Joining Date')

    @api.depends('dob','date')
    def _age(self):
        for record in self:
            if record.dob:
                dt=str(record.dob)
                d1=datetime.strptime(dt, "%Y-%m-%d").date()
                d2=record.date
                record.agecal = relativedelta(d2, d1).years


