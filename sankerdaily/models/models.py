# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_round
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)


class sankerdaily(models.Model):
    _name = 'sankerdaily.currentaccount'
    _rec_name = 'acct'
    date = fields.Date(string='Transaction Date', required=True)
    type = fields.Selection([('DEP','DEP'),('MBP','MBP')], string='Type of Transaction')
    acct = fields.Char(string='Account')
    description = fields.Char(sting='Description')
    debit = fields.Float(string='Debit')
    credit = fields.Float(string='Credit')
    detail = fields.Char(string='CHQ/ E-pay Order number')
    balance = fields.Float(string='Total Amount', compute='_balance')
    action = fields.Boolean(string='Note')    
    note = fields.Char(string='Note Details')

    @api.depends('debit', 'credit')
    def _balance(self):
        for record in self:
            record.balance = record.balance - record.debit + record.credit

class dailytakings(models.Model):
    _name = 'sankerdaily.dailytakings'
    _rec_name = 'date'
    date = fields.Date(string='Date', required=True)
    opdconsult = fields.Float(string='OPD Consulatation Fees')
    opdmed = fields.Float(string='OPD medicines')
    opdtotal = fields.Float(string='OPD Total', compute='_opdtotal')
    ipd = fields.Float(string='IPD takings')
    daycare = fields.Float(string='Daycare')
    academic = fields.Float(string='Academic Activities')
    certificates = fields.Float(string='Certificates')
    canteen = fields.Float(string='Canteen')
    handicraft = fields.Float(string='Handicraft')
    refund = fields.Float(string='Refunded to Patients')
    misc = fields.Float(string='Miscellaneous')
    total = fields.Float(string='Total Daily Takings without OP Medications', compute='_dailytotal')
    eddie = fields.Float(sting='Dr. Eddie Mukhim OP Consultation')
    eddiedue = fields.Float(string = 'EM due', compute='_eddie')
    didak = fields.Float(string = 'Dr. Dida Khonglah OP Consultation')
    didakdue = fields.Float(string ='DK due', compute ='_didak')
    slahiri = fields.Float(string = 'Dr. S. Lahiri OP Consultation')
    slahiridue = fields.Float(string ='SL due', compute ='_slahiri')
    vranee = fields.Float(string = 'Dr. V. Ranee OP Consultation')
    vraneedue = fields.Float(string ='VR due', compute ='_vranee')
    gideon = fields.Float(string = 'Dr. Gideon Rynjah OP Consultation')
    eeg = fields.Float(string = 'EEG/EMG')    
    gideondue = fields.Float(string ='GR due', compute ='_gideon')
    mhc = fields.Float(string='MHC')
    consulttotal = fields.Float(string='Consultation Total', compute='_consulttotal')
    consultfree = fields.Float(string='Free Care')
    consultbalance = fields.Float('Balance')
    consultreal = fields.Float('Real')
    consultnet = fields.Float('Net', compute='_consultnet')
    medtotal = fields.Float(string='Medicine Total', compute='_medtotal')
    medfree = fields.Float(string='Free Care')
    medbalance = fields.Float('Balance')
    medreal = fields.Float('Real')
    mednet = fields.Float('Net', compute='_mednet')
    date_start = fields.Datetime()
    date_end = fields.Datetime()

    @api.depends('opdmed','medfree','medreal', 'medbalance')
    def _medtotal(self):
        for record in self:
            record.medtotal = record.mednet + record.medfree + record.medbalance - record.medreal

    @api.depends('consultnet','consultfree','consultreal', 'consultbalance')
    def _consulttotal(self):
        for record in self:
            record.consulttotal =  record.consultnet + record.consultfree + record.consultbalance - record.consultreal

    @api.depends('opdconsult', 'eddiedue', 'didakdue', 'gideondue', 'vraneedue', 'slahiridue', 'mhc')
    def _consultnet(self):
        for record in self:
            record.consultnet = round(record.opdconsult - (record.eddiedue + record.didakdue + record.vraneedue + record.gideondue + record.slahiridue + record.mhc), -1)

    @api.depends('opdmed')
    def _mednet(self):
        for record in self:
            record.mednet = round(record.opdmed * 0.9)

    
    @api.depends('opdconsult','opdmed')
    def _opdtotal(self):
        for record in self:
            record.opdtotal = record.opdconsult + record.opdmed

    @api.depends('opdconsult','ipd','daycare','academic','certificates','canteen','handicraft','refund','misc')
    def _dailytotal(self):
        for record in self:
            record.total = record.opdconsult + record.ipd + record.daycare + record.academic + record.certificates + record.canteen + record.handicraft - record.refund - record.misc

    @api.depends('eddie')
    def _eddie(self):
        for record in self:
            record.eddiedue = record.eddie / 2

    @api.depends('didak')
    def _didak(self):
        for record in self:
            record.didakdue = record.didak/ 2

    @api.depends('slahiri')
    def _slahiri(self):
        for record in self:
            record.slahiridue = record.slahiri / 2

    @api.depends('vranee')
    def _vranee(self):
        for record in self:
            record.vraneedue = record.vranee/ 2

    @api.depends('gideon', 'eeg')
    def _gideon(self):
        for record in self:
            record.gideondue = (record.gideon/ 2) + record.eeg

    

    

    @api.multi
    def get_consult(self):
        for record in self:
            if record.date:
                date_str = record.date.strftime(DATE_FORMAT)
                date_to = record.date.strftime(DATE_FORMAT)
                date_str += " 00:00:00"
                date_to += " 23:59:59"
                record.date_start = datetime.strptime(date_str, DATETIME_FORMAT)
                record.date_end = datetime.strptime(date_to, DATETIME_FORMAT)
        _logger.info(self.date_end)
        _logger.info(self.date)
        consultations = self.env['opregistration'].search([['date','=', self.date]])
        em_consult=0
        dk_consult=0            
        sl_consult=0
        vr_consult=0
        gr_consult=0
        ep_total = 0    
        for consultation in consultations:
            if consultation.providerlink.name == 'Dr. Eddie Mukhim':
                em_consult += consultation.fee
            if consultation.providerlink.name == 'Dr. D. Khonglah':
                dk_consult += consultation.fee
            if consultation.providerlink.name == 'Dr. S. Lahiri':
                sl_consult += consultation.fee
            if consultation.providerlink.name == 'Dr. V. Ranee':
                vr_consult += consultation.fee
            if consultation.providerlink.name == 'Dr. Gideon Rynjah':
                gr_consult += consultation.fee

        electros = self.env['pos.order'].search([['date_order','>=', self.date_start],['date_order','<=', self.date_end]])
        for electro in electros:
            for electro.line in electro.lines:
                if electro.line.product_id.display_name == 'EEG':
                    ep_total += electro.line.price_subtotal_incl
                if electro.line.product_id.display_name == 'EMG':
                    ep_total += electro.line.price_subtotal_incl

                    
        for record in self:
            record.eddie = em_consult
            record.didak = dk_consult
            record.slahiri = sl_consult
            record.vranee = vr_consult
            record.eddie = em_consult
            record.gideon  = gr_consult
            record.eeg = ep_total



            



class dailyinfo(models.Model):
    _name = 'sankerdaily.dailyinfo'
    _rec_name = 'detail'
    date = fields.Date('Transaction Date', required=True)
    detail = fields.Char('Transaction Detail')
    credit = fields.Float('Credit')
    debit = fields.Float('Debit')
    total = fields.Float('Total', compute='_infototal')
    action = fields.Boolean(string='Note')    
    note = fields.Char(string='Note Details')


    @api.depends('credit','debit')
    def _infototal(self):
        for record in self:
            record.total = record.credit - record.debit
