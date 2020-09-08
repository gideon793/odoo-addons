# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class opregistration(models.Model):
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    _rec_name = 'partner_id'
    providerlink = fields.Many2one('doctors.doctors', string='Doctor')
    date = fields.Date(string='Date of Appointment', default = fields.Date.today ())
    registration = fields.Char(related='partner_id.registration',store=True)
    type = fields.Selection([('new','New'),('old','Old'),('med','Medicines only')],string='Appointment Type', default='old')
    fee  = fields.Integer(string='Consultation Fee')
    newfee = fields.Integer(related='providerlink.newfee')
    oldfee = fields.Integer(related='providerlink.oldfee')
    freecare = fields.Integer(compute='_freecare')
    diagl=fields.One2many('linediag','link')
    selectno = fields.Char(string='Enter Registration number')
    

    @api.onchange('fee','type')
    def _freecare(self):
        for record in self:
            if record.type == 'new':
                record.freecare=int(record.newfee - record.fee)
            if record.type == 'old':
                record.freecare=int(record.oldfee - record.fee)
            if record.type == 'med':
                record.freecare=int(record.oldfee - record.fee)

    @api.onchange('selectno')
    def get_partner(self):
        if self.selectno:
            partner = self.env['res.partner'].search([('registration', 'ilike', self.selectno)], limit=1)
            if partner:
                self.partner_id = partner.id


    
class linediag(models.Model):
    link=fields.Many2one('opregistration')
    diagnosis = fields.Many2one('diagnosis.diagnosis', string="diagnosis", widget='Selection')
    code = fields.Char(related='diagnosis.code', store=True)
    






    



