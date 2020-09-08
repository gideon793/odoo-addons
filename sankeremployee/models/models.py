# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,date
from dateutil.relativedelta import relativedelta


class sankeremployee(models.Model):
    _name = 'sankeremployee.sankeremployee'
    name = fields.Char('Employee Name')
    employmentno = fields.Char('Employment Number')
    dob=fields.Date('Date of Birth', related='employee.dob')
    age = fields.Integer('Age', compute="_age")
    gender = fields.Selection(related='employee.gender', string='Gender')
    address=fields.Char(related='employee.contact_address')      
    designation = fields.Char('Designation')
    joindate = fields.Date('Joining Date')
    marital_status=fields.Selection(related='employee.maritalstatus')
    basicpay = fields.Float('Basic Pay')
    allowance = fields.Float('100% Fitness Allowance', default=lambda self: self.basicpay)
    special = fields.Float(string='Special Duty Allowance')
    annualpay = fields.Float(compute='_annualpay', string='Computed Annual Pay')
    isepf = fields.Boolean('Is there an EPF Account')
    epfno = fields.Char('EPF Number')
    epfname = fields.Char('EPF Name')
    epfwage = fields.Float('EPF Wage', compute = "_epfwage")
    isesic = fields.Boolean('Is there an ESIC account')
    esicno = fields.Char('ESIC number')
    esicname = fields.Char('ESIC Name')
    esicwage = fields.Float('ESIC wages', compute="_esicwage")
    acctno = fields.Char('SBI Account Number')
    branch = fields.Char('SBI Branch Code')
    taxrate = fields.Integer(string='Professional Tax Rate', compute='_taxrate')
    professionaltaxcalc = fields.Float(string='Professional Tax', compute="_prof")
    regular = fields.Boolean('Regular Employee')
    contract = fields.Boolean('Contractual Employee')
    ddrs = fields.Boolean('DDRS Employee')
    employee = fields.Many2one('res.partner', string='Employee name')
    pan = fields.Char('PAN Number')
    aadhar = fields.Char('AADHAR Number')
    epic = fields.Char('EPIC Number')
    driving = fields.Char('Driving License')
    bloodgroup = fields.Char('Blood Group')
    remarks = fields.Text('Additional Remarks')



    def _annualpay(self):
        for record in self:
            record.annualpay = record.basicpay * 24

    def _taxrate(self):
        for record in self:
            if record.annualpay <= 50000:
                record.taxrate = 1
            if 50001 <= record.annualpay <= 75000:
                record.taxrate = 2
            if 75001 <= record.annualpay <= 100000:
                record.taxrate = 3
            if 100001 <= record.annualpay <= 150000:
                record.taxrate = 4
            if 150001 <= record.annualpay <= 200000:
                record.taxrate = 5
            if 200001 <= record.annualpay <= 250000:
                record.taxrate = 6
            if 250001 <= record.annualpay <= 300000:
                record.taxrate = 7
            if 300001 <= record.annualpay <= 350000:
                record.taxrate = 8
            if 350001 <= record.annualpay <= 400000:
                record.taxrate = 9
            if 400001 <= record.annualpay <= 450000:
                record.taxrate = 10
            if 450001 <= record.annualpay <= 500000:
                record.taxrate = 11
            if 500001 <= record.annualpay:
                record.taxrate = 12

    def _epfwage(self):
        for record in self:
            if record.basicpay <= 15000:
                record.epfwage = record.basicpay
            if 15001 <= record.basicpay:
                record.epfwage = 15000

    def _esicwage(self):
        for record in self:
            if record.basicpay <= 21000:
                record.esicwage = record.basicpay
            if 21001 <= record.basicpay:
                record.esicwage = 21000

    @api.onchange('name')
    def getepfname(self):
        if self.name:
            self.epfname = self.name
            self.esicname = self.name

    def _prof(self):
        for record in self:
            if record.taxrate == 1:
                record.professionaltaxcalc = 0
            if record.taxrate == 2:
                record.professionaltaxcalc = round(200 / 12)
            if record.taxrate == 3:
                record.professionaltaxcalc = round(300 / 12)
            if record.taxrate == 4:
                record.professionaltaxcalc = round(500 / 12)
            if record.taxrate == 5:
                record.professionaltaxcalc = round(750 / 12)
            if record.taxrate == 6:
                record.professionaltaxcalc = round(1000 / 12)
            if record.taxrate == 7:
                record.professionaltaxcalc = round(1250 / 12)
            if record.taxrate == 8:
                record.professionaltaxcalc = round(1500 / 12)
            if record.taxrate == 9:
                record.professionaltaxcalc = round(1800 / 12)
            if record.taxrate == 10:
                record.professionaltaxcalc = round(2100 / 12)
            if record.taxrate == 11:
                record.professionaltaxcalc = round(2400 / 12)
            if record.taxrate == 12:
                record.professionaltaxcalc = round(2500 / 12)


    @api.depends('dob')
    def _age(self):
        for record in self:
            if record.dob:
                dt=str(record.dob)
                d1=datetime.strptime(dt, "%Y-%m-%d").date()
                d2=date.today()
                record.age = relativedelta(d2, d1).years

    @api.multi
    def update_ages(self):
        for record in self.env['sankeremployee.sankeremployee'].search([]):
            if record.agecal:
                dt=str(record.dob)
                d1=datetime.strptime(dt, "%Y-%m-%d").date()
                d2=date.today()
                record.age = relativedelta(d2, d1).years

