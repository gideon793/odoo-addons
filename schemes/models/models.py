# -*- coding: utf-8 -*-

from odoo import models, fields, api

class schemes(models.Model):
    _name = 'schemes.schemes'
    name = fields.Char(string='Name')
    father = fields.Char('Father\'s Name')
    dob = fields.Date('Date of Birth')
    gender = fields.Selection([('male','Male'),('female','Female')], string='Gender')
    designation = fields.Char('Designation')
    address = fields.Char('Address')
    education = fields.Char('Educational Qualifications')
    appointdate = fields.Date('Date of Appointment')
    employment = fields.Char('Period of Appointment in months')
    honorarium = fields.Float('Honorarium per month')
    paid = fields.Float('Total Honorarium paid during the year')
    proposed = fields.Float('Total Honorarium proposed in the current year')
    category=fields.Selection([('gen','General'),('st','ST'),('sc','SC'),('obc','OBC')], string='Category')
    aadhar = fields.Char('AADHAR number')
    mobile = fields.Char('Mobile Number')
    email = fields.Char('Email address')
    bankacc = fields.Char('Bank Account number')
    bankifsc = fields.Char('Bank IFSC code')
    bankbranch = fields.Char('Bank Branch')
    aadharseeded = fields.Char('AADHAR seeded bank acc')






