# -*- coding: utf-8 -*-

from odoo import models, fields, api

class doctors(models.Model):
    _name = 'doctors.doctors'
    _order='name asc'
    name = fields.Char(string='Name of the Provider')
    department = fields.Selection([('psychiatry','Psychiatry'),('neurology','Neurology'),('psychology','Clinical Psychology'),('physiotherapy','Physiotherapy')],string='Dpeartment')
    newfee = fields.Integer(string='Consultation Fee for New Patients')
    oldfee = fields.Integer(string='Consultation Fee for Review Patients')
    qualification = fields.Char (string='Qualifications')
    medreg = fields.Char(string='Registration no.')
