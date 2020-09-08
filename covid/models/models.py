# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)


class covid(models.Model):
    _name = 'covid.covid'
    _description = 'Module for research project on Covid-19'
    _rec_name='partner_id'
    date = fields.Date('Date')
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    registration = fields.Char(related='partner_id.registration',store=True)
    age = fields.Integer(related='partner_id.agecal')
    gender = fields.Selection (related='partner_id.gender')
    diagnosis = fields.One2many(related = 'partner_id.pat_diag')
    type = fields.Selection([('focal','Focal Epilepsy'),('generalized','Generalized Epilepsy'),('combined','Combined'),('unknown','Unknown')], 'Type of Epilepsy')
    etiology = fields.Selection([('structural','Structural'),('genetic','Genetic'),('infect','Infectious'),('metabolic','Metabolic'),('immune','Immune'),('unknown','Unknown')],'Etiology')
    refractory = fields.Boolean('Refractory Epilepsy?')
    medications = fields.Integer('Number of Medications')
    control = fields.Boolean('Previously well controlled?')
    lastseizure = fields.Float('Previous seizure in months')
    seizure = fields.Boolean('Seizure at this visit?')
    status = fields.Boolean('Status epilepticus?')
    default = fields.Boolean('Drug Default?')

class statistics(models.TransientModel):
    _name = 'covid.statistics'
    _description = 'Module for OPD Statisctics'
    startdateentry = fields.Date(string='Start date')
    enddateentry = fields.Date(string='End date')

           
    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'startdate': self.startdateentry,
                'enddate': self.enddateentry,
            },
        }
        return self.env.ref('covid.statistics_report').report_action(self, data=data)


class opdstatisticsreport(models.AbstractModel):
    _name = 'report.covid.statistics_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        startdate=data['form']['startdate']
        enddate=data['form']['enddate']
        _logger.info('Report')
        _logger.info(startdate)
        _logger.info(enddate)
        male_child=0
        female_child=0
        male_adult=0
        female_adult=0
        male_elderly=0
        female_elderly=0
        appts  = self.env['opregistration'].search([['date','>=',startdate],['date','<=',enddate]], order='create_date')
        for appt in appts:
            _logger.info(appt.partner_id.gender)
            _logger.info(appt.agecal)
            if (appt.partner_id.gender == 'male') and (appt.agecal < 18):
                male_child +=1
            if (appt.partner_id.gender == 'female') and (appt.agecal < 18):
                female_child +=1
            if (appt.partner_id.gender == 'male') and (18 <= appt.agecal < 60):
                male_adult +=1
            if (appt.partner_id.gender == 'female') and (18 <= appt.agecal < 60):
                female_adult +=1
            if (appt.partner_id.gender == 'male') and (60< appt.agecal):
                male_elderly +=1
            if (appt.partner_id.gender == 'female') and (60< appt.agecal):
                female_elderly +=1
        child_total = male_child + female_child
        adult_total = male_adult + female_adult
        elderly_total = male_elderly + female_elderly
        total = child_total + adult_total + elderly_total
        male_total = male_child + male_adult + male_elderly
        female_total = female_child + female_adult + female_elderly


        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'startdate': startdate,
            'enddate': enddate,
            'male_child': male_child,
            'female_child': female_child,
            'male_adult': male_adult,
            'female_adult': female_adult,
            'male_elderly': male_elderly,
            'female_elderly': female_elderly,
            'child_total' : child_total,
            'adult_total' : adult_total,
            'elderly_total': elderly_total,
            'total': total,
            'male_total': male_total,
            'female_total': female_total


        }


class ipdstatistics(models.TransientModel):
    _name = 'covid.ipdstatistics'
    _description = 'Module for IPD Statisctics'
    startdateentry = fields.Date(string='Start date')
    enddateentry = fields.Date(string='End date')

           
    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'startdate': self.startdateentry,
                'enddate': self.enddateentry,
            },
        }
        return self.env.ref('covid.ipdstatistics_report').report_action(self, data=data)

class ipdstatisticsreport(models.AbstractModel):
    _name = 'report.covid.ipdstatistics_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        startdate=data['form']['startdate']
        enddate=data['form']['enddate']
        _logger.info('IPD Report')
        _logger.info(startdate)
        _logger.info(enddate)
        male_child=0
        female_child=0
        male_adult=0
        female_adult=0
        male_elderly=0
        female_elderly=0
        appts  = self.env['admission'].search([['admdate','>=',startdate],['admdate','<=',enddate]], order='create_date')
        for appt in appts:
            _logger.info(appt.partner_id.gender)
            _logger.info(appt.agecal)
            if (appt.partner_id.gender == 'male') and (appt.agecal < 18):
                male_child +=1
            if (appt.partner_id.gender == 'female') and (appt.agecal < 18):
                female_child +=1
            if (appt.partner_id.gender == 'male') and (18 <= appt.agecal < 60):
                male_adult +=1
            if (appt.partner_id.gender == 'female') and (18 <= appt.agecal < 60):
                female_adult +=1
            if (appt.partner_id.gender == 'male') and (60< appt.agecal):
                male_elderly +=1
            if (appt.partner_id.gender == 'female') and (60< appt.agecal):
                female_elderly +=1
        child_total = male_child + female_child
        adult_total = male_adult + female_adult
        elderly_total = male_elderly + female_elderly
        total = child_total + adult_total + elderly_total
        male_total = male_child + male_adult + male_elderly
        female_total = female_child + female_adult + female_elderly


        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'startdate': startdate,
            'enddate': enddate,
            'male_child': male_child,
            'female_child': female_child,
            'male_adult': male_adult,
            'female_adult': female_adult,
            'male_elderly': male_elderly,
            'female_elderly': female_elderly,
            'child_total' : child_total,
            'adult_total' : adult_total,
            'elderly_total': elderly_total,
            'total': total,
            'male_total': male_total,
            'female_total': female_total


        }


