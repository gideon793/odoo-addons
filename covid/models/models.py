# -*- coding: utf-8 -*-
from typing import Dict, List, Any

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging

_logger = logging.getLogger(__name__)
from dateutil.relativedelta import relativedelta
from io import BytesIO, StringIO
import xlwt
import base64


class covid(models.Model):
    _name = 'covid.covid'
    _description = 'Module for research project on Covid-19'
    _rec_name = 'partner_id'
    date = fields.Date('Date')
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    registration = fields.Char(related='partner_id.registration')
    dob = fields.Date(related='partner_id.dob')
    agecal = fields.Integer(compute='_age', store=True, group_operator=False)
    gender = fields.Selection(related='partner_id.gender')
    diagnosis = fields.One2many(related='partner_id.pat_diag')
    type = fields.Selection(
        [('focal', 'Focal Epilepsy'), ('generalized', 'Generalized Epilepsy'), ('combined', 'Combined'),
         ('unknown', 'Unknown')], 'Type of Epilepsy')
    etiology = fields.Selection(
        [('structural', 'Structural'), ('genetic', 'Genetic'), ('infect', 'Infectious'), ('metabolic', 'Metabolic'),
         ('immune', 'Immune'), ('unknown', 'Unknown')], 'Etiology')
    refractory = fields.Boolean('Refractory Epilepsy?')
    medications = fields.Integer('Number of Medications')
    control = fields.Boolean('Previously well controlled?')
    lastseizure = fields.Float('Previous seizure in months')
    seizure = fields.Boolean('Seizure at this visit?')
    status = fields.Boolean('Status epilepticus?')
    default = fields.Boolean('Drug Default?')
    default_duration = fields.Float('Duration of Default in Days')
    medication_list = fields.Text('Medication List')
    onset = fields.Char('Onset of Seizures')

    @api.depends('dob', 'date')
    def _age(self):
        for record in self:
            if record.dob:
                dt = str(record.dob)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = record.date
                record.agecal = relativedelta(d2, d1).years


class didaresearch(models.Model):
    _name = 'covid.didaresearch'
    _description = 'Module for research project on Covid-19 - pyschotropic drugs'
    _rec_name = 'partner_id'
    date = fields.Date('Date of Admission')
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    occupation = fields.Char(related='partner_id.occupation')
    registration = fields.Char(related='partner_id.registration', store=True)
    age = fields.Integer(related='partner_id.agecal')
    gender = fields.Selection(related='partner_id.gender')
    antipsychotic = fields.Boolean('Antipsychotics?')
    antipsychoticdetails = fields.Text('Details')
    antidepressant = fields.Boolean('Antidepressants?')
    antidepressantdetails = fields.Text('Details')
    anxiolytic = fields.Boolean('Anxiolytics?')
    anxiolyticdetails = fields.Text('Details')
    antiepileptic = fields.Boolean('Antiepileptics?')
    antiepilepticdetails = fields.Text('Details')
    moodstabilizer = fields.Boolean('Mood Stabilizers?')
    moodstabilizerdetails = fields.Text('Details')
    others = fields.Text('Others')
    diagnosis = fields.One2many(related='partner_id.pat_diag')
    comorbid = fields.Boolean('Any comorbidities?')
    details = fields.Text('Details of Comorbities')
    risk = fields.Selection([('high', 'High Risk'), ('low', 'Low Risk'), ('unknown', 'Unknown')], 'Level of Risk')
    ward = fields.Selection([('male', 'Male Ward'), ('female', 'Female Ward'), ('unknown', 'Unknown')], 'Ward')
    covid = fields.Selection([('positive', 'Positive'), ('negative', 'Negative'), ('unknown', 'Unknown')],
                             'Covid Status')
    quarantine = fields.Selection(
        [('sanker', 'SAN-KER'), ('home', 'Home'), ('hospital', 'Other Hospital'), ('unknown', 'Unknown')],
        'Site of Quarantine', default='sanker')


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
        startdate = data['form']['startdate']
        enddate = data['form']['enddate']
        _logger.info('Report')
        _logger.info(startdate)
        _logger.info(enddate)
        male_child = 0
        female_child = 0
        male_adult = 0
        female_adult = 0
        male_elderly = 0
        female_elderly = 0
        appts = self.env['opregistration'].search([['date', '>=', startdate], ['date', '<=', enddate]],
                                                  order='create_date')
        for appt in appts:
            _logger.info(appt.partner_id.gender)
            _logger.info(appt.agecal)
            if (appt.partner_id.gender == 'male') and (appt.agecal < 18):
                male_child += 1
            if (appt.partner_id.gender == 'female') and (appt.agecal < 18):
                female_child += 1
            if (appt.partner_id.gender == 'male') and (18 <= appt.agecal < 60):
                male_adult += 1
            if (appt.partner_id.gender == 'female') and (18 <= appt.agecal < 60):
                female_adult += 1
            if (appt.partner_id.gender == 'male') and (60 < appt.agecal):
                male_elderly += 1
            if (appt.partner_id.gender == 'female') and (60 < appt.agecal):
                female_elderly += 1
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
            'child_total': child_total,
            'adult_total': adult_total,
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
        startdate = data['form']['startdate']
        enddate = data['form']['enddate']
        _logger.info('IPD Report')
        _logger.info(startdate)
        _logger.info(enddate)
        male_child = 0
        female_child = 0
        male_adult = 0
        female_adult = 0
        male_elderly = 0
        female_elderly = 0
        appts = self.env['admission'].search([['admdate', '>=', startdate], ['admdate', '<=', enddate]],
                                             order='create_date')
        for appt in appts:
            _logger.info(appt.partner_id.gender)
            _logger.info(appt.agecal)
            if (appt.partner_id.gender == 'male') and (appt.agecal < 18):
                male_child += 1
            if (appt.partner_id.gender == 'female') and (appt.agecal < 18):
                female_child += 1
            if (appt.partner_id.gender == 'male') and (18 <= appt.agecal < 60):
                male_adult += 1
            if (appt.partner_id.gender == 'female') and (18 <= appt.agecal < 60):
                female_adult += 1
            if (appt.partner_id.gender == 'male') and (60 < appt.agecal):
                male_elderly += 1
            if (appt.partner_id.gender == 'female') and (60 < appt.agecal):
                female_elderly += 1
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
            'child_total': child_total,
            'adult_total': adult_total,
            'elderly_total': elderly_total,
            'total': total,
            'male_total': male_total,
            'female_total': female_total
        }


class rattest(models.Model):
    _name = 'covid.rattest'
    date = fields.Date('Date', default=fields.Date.today)
    name = fields.Many2one('res.partner', 'Name')
    dob = fields.Date(related='name.dob')
    age = fields.Integer(compute='_age')
    gender = fields.Selection(related='name.gender')
    address = fields.Char(default='SAN-KER')
    occupation = fields.Char('Occupation')
    phone = fields.Char('Mobile No')
    travel = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', string='Travel History')
    arrivaldate = fields.Char(string='Arrival Date', default='NA')
    contact = fields.Selection([('no', 'No'), ('yes', 'Yes')], default='no',
                               string='History of Contact with confirmed case')
    case = fields.Char(string='Name of Confirmed Case', default='NA')
    symptoms = fields.Char(string='Symptoms', default='None')
    comorbidities = fields.Char(string='Comorbities', default='None')
    vaccination = fields.Selection([('no', 'No'), ('yes', 'Yes')], default='no', string='Vaccination History')
    result = fields.Selection([('negative', 'Negative'), ('positive', 'Positive')], default='negative')

    @api.onchange('name')
    def get_occupation(self):
        for record in self:
            record.occupation = record.name.occupation
            record.phone = record.name.mobile

    @api.depends('dob', 'date')
    def _age(self):
        for record in self:
            if record.dob:
                dt = str(record.dob)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = record.date
                record.age = relativedelta(d2, d1).years


class rattest_wizard(models.TransientModel):
    _name = 'covid.rattestwizard'
    date = fields.Date(default=fields.Date.today, string='Report Date')
    file = fields.Binary('XLS File', readonly=True)
    filename = fields.Char('Name')

    @api.multi
    def get_excel_report(self):
        fp = BytesIO()
        workbook = xlwt.Workbook(encoding='utf-8')
        writer = workbook.add_sheet('RAT Test Report Daily %s' % (self.date.strftime("%d-%m-%y")),
                                    cell_overwrite_ok=True)
        style_bold = "font: bold on"
        style_normal = "font: bold off"
        bold = xlwt.easyxf(style_bold)
        normal = xlwt.easyxf(style_normal)
        row = 0
        column = 0
        for x in range(10):
            writer.col(x).width = 256 * 20
        writer.write(row, column, "Serial No.", bold)
        writer.write(row, column + 1, "Name", bold)
        writer.write(row, column + 2, "Age", bold)
        writer.write(row, column + 3, "Gender", bold)
        writer.write(row, column + 4, "Address", bold)
        writer.write(row, column + 5, "Occupation", bold)
        writer.write(row, column + 6, "Mobile No.", bold)
        writer.write(row, column + 7, "Any Travel History", bold)
        writer.write(row, column + 8, "Arrival Date", bold)
        writer.write(row, column + 9, "Any History of Contact", bold)
        writer.write(row, column + 10, "Name of the Confirmed Case", bold)
        writer.write(row, column + 11, "Any Symptoms", bold)
        writer.write(row, column + 12, "Any Comorbidities", bold)
        writer.write(row, column + 13, "Covid Vaccination History", bold)
        writer.write(row, column + 14, "Rat Result", bold)

        appts = self.env['covid.rattest'].search([['date', '=', self.date]])

        for appt in appts:
            if appt.gender == 'male':
                sex = 'Male'
            elif appt.gender == 'female':
                sex = 'Female'
            if appt.travel == 'no':
                travel = 'No'
            elif appt.travel == 'yes':
                travel = 'Yes'
            if appt.vaccination == 'no':
                vaccination = 'No'
            elif appt.vaccination == 'yes':
                vaccination = 'Yes'
            if appt.contact == 'no':
                contact = 'No'
            elif appt.contact == 'yes':
                contact = 'Yes'

            if appt.result == 'negative':
                result = 'Negative'
            elif appt.result == 'positive':
                result = 'Positive'

            column = 0
            row += 1
            writer.write(row, column, row, normal)
            writer.write(row, column + 1, appt.name.name, normal)
            writer.write(row, column + 2, appt.age, normal)
            writer.write(row, column + 3, sex, normal)
            writer.write(row, column + 4, appt.address, normal)
            writer.write(row, column + 5, appt.occupation, normal)
            writer.write(row, column + 6, appt.phone, normal)
            writer.write(row, column + 7, travel, normal)
            writer.write(row, column + 8, appt.arrivaldate, normal)
            writer.write(row, column + 9, contact, normal)
            writer.write(row, column + 10, appt.case, normal)
            writer.write(row, column + 11, appt.symptoms, normal)
            writer.write(row, column + 12, appt.comorbidities, normal)
            writer.write(row, column + 13, vaccination, normal)
            writer.write(row, column + 14, result, normal)

        workbook.save(fp)
        self.file = base64.b64encode(fp.getvalue())
        self.filename = self.id
        return {
            'name': 'RAT TEST Excel Report',
            'type': 'ir.actions.act_url',
            'url': '/web/content/covid.rattestwizard/%s/file/san_ker_rattest.xls?download=true' % (self.id),
            'target': 'new',
        }

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date': self.date
            },
        }
        return self.env.ref('covid.dhmo_report').report_action(self, data=data)


class dmhoreport(models.AbstractModel):
    _name = 'report.covid.dmhoreport'

    @api.multi
    def _get_report_values(self, docids, data=None):
        date = data['form']['date']
        _logger.info(date)
        details = []
        tests = self.env['covid.rattest'].search([['date', '=', date]])
        _logger.info(tests)

        for x in tests:
            _logger.info(x.name)
            details.append({
                'name': x.name.name,
                'gender': x.gender,
                'age': x.age,
                'address': x.address,
                'occupation': x.occupation,
                'phone': x.phone,
                'travel': x.travel,
                'arrivaldate': x.arrivaldate,
                'contact': x.contact,
                'travel': x.travel,
                'arrivaldate': x.arrivaldate,
                'contact': x.contact,
                'case': x.case,
                'symptoms': x.symptoms,
                'comorbidities': x.comorbidities,
                'vaccination': x.vaccination,
                'result': x.result,
                'id': x.id
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date': date,
            'details': details,
        }


class epilepsy(models.Model):
    _name = 'covid.epilepsy'
    _description = 'Epilepsy Patient Details'
    _rec_name = 'partner_id'
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    registration = fields.Char(related='partner_id.registration')
    dob = fields.Date(related='partner_id.dob')
    gender = fields.Selection(related='partner_id.gender')
    diagnosis = fields.One2many(related='partner_id.pat_diag')
    type = fields.Selection(
        [('focal', 'Focal Epilepsy'), ('generalized', 'Generalized Epilepsy'), ('combined', 'Combined'),
         ('unknown', 'Unknown')], 'Type of Epilepsy')
    etiology = fields.Selection(
        [('structural', 'Structural'), ('genetic', 'Genetic'), ('infect', 'Infectious'), ('metabolic', 'Metabolic'),
         ('immune', 'Immune'), ('unknown', 'Unknown')], 'Etiology')
    refractory = fields.Boolean('Refractory Epilepsy?')
    medications = fields.Integer('Number of Medications')
    control = fields.Boolean('Well controlled?')
    medication_list = fields.Text('Medication List')
    onset = fields.Char('Onset of Seizures')
    last_attack = fields.Date('Last Seizure Reported')
    eeg = fields.Selection(
        [('focal', 'Focal ED'), ('generalized', 'Generalized ED'), ('other', 'Other'), ('normal', 'Normal'),
         ('na', 'Not Available')], 'EEG Findings')
    imaging = fields.Boolean('Abnormal Imaging?')
    imaging_details = fields.Char('Imaging Details')
