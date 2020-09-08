# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)




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
    dob = fields.Date(related='partner_id.dob')
    agecal = fields.Integer(compute='_age',store=True, group_operator=False)
    address=fields.Char(related='partner_id.contact_address')      
    gender = fields.Selection(related = 'partner_id.gender')

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
    
    @api.depends('dob','date')
    def _age(self):
        for record in self:
            if record.dob:
                dt=str(record.dob)
                d1=datetime.strptime(dt, "%Y-%m-%d").date()
                d2=record.date
                record.agecal = relativedelta(d2, d1).years
   
    @api.onchange('partner_id')
    def checkname(self): 
        exists= self.env['res.partner'].search([('name', '=', self.partner_id.name),('id','!=',self.partner_id.id)])
        if exists:
            return {
        'name': 'view_opregistration_warning',
        'type': 'ir.actions.act_window',
        'res_model': 'opregistration.warning',
        'view_mode': 'form',
        'view_id': 'view_opregistration_warning',
        'target': 'new'
      }



class linediag(models.Model):
    link=fields.Many2one('opregistration')
    diagnosis = fields.Many2one('diagnosis.diagnosis', string="diagnosis", widget='Selection')
    code = fields.Char(related='diagnosis.code', store=True)

class warningmessage(models.TransientModel):
    _name='opregistration.warning'
    _description = 'Opregistration Warning Message'
    message = fields.Text('message')


    



 


    



