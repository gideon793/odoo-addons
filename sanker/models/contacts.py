# -*- coding: utf-8 -*-

from odoo import api,models, fields
from datetime import datetime,date
from dateutil.relativedelta import relativedelta



class patients(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string='Gender')
    registration = fields.Char('Registration number')
    religion = fields.Char('Religion')
    maritalstatus = fields.Selection([('single','Single'), ('married','Married'),('separated','Separated'), ('divorced','Divorced'),('widowed','Widowed')],string='Marital Status')
    relative = fields.Text(string='Contact Person')
    relativephone = fields.Char(string='Contact Person phone number')
    religion = fields.Selection([('christian-p','Christianity - Presbyterian'),('christian-c','Christianity - Roman Catholic'),('christian-o','Christianity - others'),('khasi','Niam Khasi'),('niamtre','Niam Tre'),('hindu','Hinduism'),('islam','Islam'),('buddhism','Buddhism'),('others','Others')])
    education = fields.Selection([('uneducated','No formal Education'),('primary','Upto Class 5'),('secondary','Upto Class 10'),('higher','Upto Class 12'),('graduate','Graduate'),('postgraduate','Post-graduate/Higher'),('professional','Professional')])
    ipregno = fields.Char('IP Registration')
    occupation = fields.Char('Occupation')
    pat_diag = fields.One2many('sanker.diagnosis','patdiagnosis', string='Diagnosis')
    district = fields.Selection([('shillong','East Khasi Hills - Shillong'), ('ekh','East Khasi Hills - outside Shillong'), ('wkh','West Khasi Hills'), ('swkh','South West Khasi Hills'), ('rbd','Ri Bhoi District'), ('wjh','West Jaintia Hills'), ('ejh','East Jaintia Hills'), ('wgh','West Garo Hills'), ('egh','East Garo Hills'), ('ngh','North Garo Hills'), ('sgh','South Garo Hills'), ('swgh','South West Garo Hills'), ('others','Outside Meghalaya')], string='District')

class diagnosis(models.Model):
    _name = 'sanker.diagnosis'
    patdiagnosis = fields.Many2one('res.partner')
    diagnosis = fields.Many2one('diagnosis.diagnosis', string="diagnosis", widget='Selection')
    code = fields.Char(related='diagnosis.code', store=True)



