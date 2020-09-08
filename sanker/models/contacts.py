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

