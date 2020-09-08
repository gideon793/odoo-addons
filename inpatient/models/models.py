# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inpatient(models.Model):
    partner_id= fields.Many2one('res.partner', string='Patient name')
    _rec_name = 'partner_id'
    registration = fields.Char(related='partner_id.registration')
    ipregno = fields.Char(related='partner_id.ipregno')
    age = fields.Integer(related='partner_id.age')
    gender = fields.Selection(related='partner_id.gender')
    admlink = fields.One2many('admission','link')


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



class ipsale(models.Model):
    _inherit = 'sale.order'
    admlink = fields.Many2one('admission') 

class ipdiag(models.Model):
    link=fields.Many2one('admission')
    diagnosis = fields.Many2one('diagnosis.diagnosis', string="diagnosis", widget='Selection')
    code = fields.Char(related='diagnosis.code', store=True)
    
