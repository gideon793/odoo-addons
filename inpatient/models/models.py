# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class inpatient(models.Model):
    partner_id= fields.Many2one('res.partner', string='Patient name')
    _rec_name = 'partner_id'
    registration = fields.Char(related='partner_id.registration')
    ipregno = fields.Char(related='partner_id.ipregno')
    gender = fields.Selection(related='partner_id.gender')
    admlink = fields.One2many('admission','link')
    credit = fields.Monetary(related='partner_id.credit')
    ward = fields.Selection([('male','Male Ward'),('female','Female Ward'), ('halfway','Halfway Home')])
    admitted = fields.Boolean('Admitted')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    agecal = fields.Integer(related='partner_id.agecal', string='Age')






class admission(models.Model): 
    admdate = fields.Date(string='Date of Admission')
    discdate = fields.Date(string='Date of Discharge')
    link=fields.Many2one('inpatient',hidden='1')
    partner_id= fields.Many2one('res.partner', string='Patient name')
    ipsaleline=fields.One2many('sale.order','admlink')
    registration = fields.Char(related='partner_id.registration')
    ipregno = fields.Char(related='partner_id.ipregno')
    advice = fields.Text(string='Advice on Discharge')
    diagip=fields.One2many('ipdiag','link')
    doctor=fields.Many2one('doctors.doctors', string='Discharging Doctor')
    dob = fields.Date(related='partner_id.dob')
    agecal = fields.Integer(compute='_age',store=True, group_operator=False, string='Age')

    @api.depends('dob','admdate')
    def _age(self):
        for record in self:
            if record.dob:
                dt=str(record.dob)
                d1=datetime.strptime(dt, "%Y-%m-%d").date()
                d2=record.admdate
                record.agecal = relativedelta(d2, d1).years





class ipsale(models.Model):
    _inherit = 'sale.order'
    admlink = fields.Many2one('admission') 

class ipdiag(models.Model):
    link=fields.Many2one('admission')
    diagnosis = fields.Many2one('diagnosis.diagnosis', string="diagnosis", widget='Selection')
    code = fields.Char(related='diagnosis.code', store=True)
    
