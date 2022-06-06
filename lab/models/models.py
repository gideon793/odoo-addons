# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging
import json
import urllib.request
from checkdigit import gs1
import socket
_logger = logging.getLogger(__name__)


class labvisit(models.Model):
    _name = 'lab.labvisit'
    _rec_name = 'labno'
    partner_id = fields.Many2one('res.partner')
    labno = fields.Char('LabNo', default='New', readonly=True, required=True, copy=False)
    date = fields.Date(string='Date of Appointment', default=fields.Date.today())
    registration = fields.Char(related='partner_id.registration', store=True)
    dob = fields.Date(related='partner_id.dob', store=True)
    agecal = fields.Integer(compute='_age', store=True, group_operator=False)
    address = fields.Char(related='partner_id.contact_address')
    gender = fields.Selection(related='partner_id.gender', store=True)
    name = fields.Char(string='Name', related='partner_id.name', store=True)
    doctor = fields.Selection([('ssyiem', 'Dr. S. Syiem'), ('eddie', 'Dr. E. Mukhim'), ('didak', 'Dr. D. Khonglah'),
                               ('gideon', 'Dr. G. Rynjah'), ('rlaloo', 'Dr. R. Laloo'),
                               ('lashngain', 'Dr.  L. Sohliya'), ('dkynjin', 'Dr. D. Kynjin'),
                               ('self', 'Self'), ('other', 'Other')], string='Doctor')
    results = fields.One2many('lab.visitresults', 'labvisit', string='Hematology Results')

    biochemresults = fields.One2many('lab.biochemresults','labvisit', string='Biochemistry Results')

    @api.depends('dob', 'date')
    def _age(self):
        for record in self:
            if record.dob:
                dt = str(record.dob)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = record.date
                record.agecal = relativedelta(d2, d1).years
    
    @api.model
    def create(self, vals):
        if vals.get('labno', 'New') == 'New':
            vals['labno'] = self.env['ir.sequence'].next_by_code('lab.labvisit') or 'New'
            check = gs1.calculate(vals['labno'])
            vals['labno'] += check
        result = super(labvisit, self).create(vals)
        return result

#    def _reset_token_number_sequences(self):
        # just use write directly on the result this will execute one update query
#        sequences = self.env['ir.sequence'].search([('name', '=like', '%labvisit%')])
#        sequences.write({'number_next_actual': 1})

    @api.multi
    def barcode(self):
        _logger.info('Button for printing barcode')
        for record in self:
            printno = bytes(record.labno, 'utf8')
            _logger.info(printno)
            self.bar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.bar.connect(('192.168.2.50', 10005))
            self.bar.sendall(printno)

    #Biochem Section
    liver = fields.Boolean('Liver Function Tests')
    tb = fields.Boolean('Total Bilirubin')
    db = fields.Boolean('Direct Bilirubin')
    sgot = fields.Boolean('SGOT')
    sgpt = fields.Boolean('SGPT')
    protein = fields.Boolean('Total Protein')
    albumin = fields.Boolean('Albumin')
    urea = fields.Boolean('Urea')
    creat = fields.Boolean('Creatinine')
    rbs = fields.Boolean('Blood Sugar')
    hba1c = fields.Boolean('HbA1C')
    uricacid = fields.Boolean('Uric Acid')
    cpk = fields.Boolean('CPK')
    lipid = fields.Boolean('Lipid Profile')
    iron = fields.Boolean('Iron')
    ferritin = fields.Boolean('Ferritin')
    kft = fields.Boolean('Renal Function Tests')

    #Biochem Results
    #LFT
    totalbil_result=fields.Char('Total Bilirubin')
    db_result = fields.Char('Direct Bilirubin')
    sgot_result = fields.Char('SGOT')
    sgpt_result = fields.Char('SGPT')
    protein_result = fields.Char('Total Protein')
    albumin_result = fields.Char('Albumin')
    alp_result = fields.Char('Alkaline Phosphatase')
    #KFT
    urea_result = fields.Char('Urea')
    creat_result = fields.Char('Creatinine')
    #Sugars
    rbs_result = fields.Char('Random Blood Sugar')
    fbs_result = fields.Char('Fasting Blood Sugar')
    ppbs_result = fields.Char('Post Prandial Blood Sugar')
    hba1c_result = fields.Char('HbA1C')
    #MISC
    uricacid_result = fields.Char('Uric Acid')
    cpk_result = fields.Char('CPK')
    amylase_result = fields.Char('Amylase')
    totchol_result = fields.Char('Total Cholestrol')
    crp_result = fields.Char('CRP')
    #LIPID
    hdl_result = fields.Char('HDL')
    ldl_result = fields.Char('LDL')
    triglyceride_result = fields.Char('Triglycerides')
    vldl_result = fields.Char('VLDL')

    #electrolyes
    sodium= fields.Char('Sodium')
    potassium= fields.Char('Potassium')
    calcium = fields.Char('Calcium')
    lithium = fields.Char('Lithium')
    phosphorus = fields.Char('Phosphorus')

    #viral markers
    hiv = fields.Selection([('neg','Negative'),('pos','Positive')],'HIV')
    hbsag = fields.Selection([('neg','Negative'),('pos','Positive')],'HBsAg')
    hcv = fields.Selection([('neg','Negative'),('pos','Positive')],'Anti-HCV')
    tpha = fields.Selection([('neg','Negative'),('pos','Positive')],'TPHA')

    #CLIA Section
    tsh_result = fields.Char('TSH')
    t3_result = fields.Char('T3 - Total')
    t4_result = fields.Char('T4-Total')
    vitb12_result = fields.Char('Vitamin B12')
    vitd_result = fields.Char('Vitamin D')

    @api.onchange('liver')
    def lft(self):
        for record in self:
            if record.liver == True:
                record.tb = True
                record.db = True
                record.sgpt = True
                record.sgot = True
                record.protein = True
                record.albumin = True
            elif record.liver == False:
                record.tb = False
                record.db = False
                record.sgpt = False
                record.sgot = False
                record.protein = False
                record.albumin = False

    @api.onchange('kft')
    def kftrecord(self):
        for record in self:
            if record.kft == True:
                record.urea = True
                record.creat = True
            if record.kft == False:
                record.urea = False
                record.creat = False
    @api.multi
    def write(self, vals):
        res = super(labvisit, self).write(vals)
        tests=[]
        for record in self:
            if record.tb == True:
                tests.append('1')
            if record.db == True:
                tests.append('2')
            if record.sgot == True:
                tests.append('3')
            if record.sgpt == True:
                tests.append('4')
            if record.protein == True:
                tests.append('5')
            if record.albumin == True:
                tests.append('6')
            if record.urea== True:
                tests.append('7')
            if record.creat == True:
                tests.append('8')
            if record.rbs== True:
                tests.append('9')
            if record.hba1c== True:
                tests.append('10')
            if record.uricacid == True:
                tests.append('11')
            if record.cpk== True:
                tests.append('12')
            if record.lipid== True:
                tests.append('13')
            if record.iron== True:
                tests.append('14')
            if record.ferritin == True:
                tests.append('15')
        _logger.info(tests)
                
        for inv in record.results:
            if inv.name == 'ESR':
                inv.units = 'mm/Hr'
                inv.range = '5-10mm/Hr'
                inv.labno = record.labno
                _logger.info('Lab No.', inv.labno)
        return res

    #Misc Results - Temporary
    miscresults = fields.One2many('lab.miscresults','labvisit')
    upt_report = fields.Char('Urine Beta HCG')
    rf_report = fields.Char('Rheumatoid Factor')

    #Hematology Section
    hemoglobin = fields.Char('Hemoglobin')
    tlc = fields.Char('Total Count')
    neutrophils = fields.Char('Neutrophils')
    lymphocytes = fields.Char('Lymphocytes')
    basophils = fields.Char('Basophils')
    eosinophils = fields.Char('Eosinophils')
    monocytes = fields.Char('Monocytes')
    platelets = fields.Char('Platelets')
    mcv = fields.Char('MCV')
    mch = fields.Char('MCH')
    mchc = fields.Char('MCHC')
    rdw_cv = fields.Char('RDW_CV')
    rdw_sd = fields.Char('RDW_SD')
    esr = fields.Char('ESR')
    pcv = fields.Char('PCV')
    rbc = fields.Char('RBC')

    #Urine Routine Section
    ure_urobilinogen  = fields.Selection([('0','Negative'),('1','+'),('2','++'),('3','+++')],'Urobilinogen')
    ure_bilirubin = fields.Selection([('0','Negative'),('1','+'),('2','++'),('3','+++')],'Bilirubin')
    ure_ketone = fields.Selection([('0','Negative'),('1','+/-'),('2','+'),('3','++'),('4','+++'),('5','++++')],'Ketone')
    ure_blood = fields.Selection([('0','Negative'),('1','+'),('2','++'),('3','+++'),('4','+/- Hemolysed'), ('5','+/- Nonhemolysed')],'Blood')
    ure_protein = fields.Selection([('0','Negative'),('1','+'),('2','++'),('3','+++'),('4','++++'),('5','+/-')],'Protein')
    ure_nitrite = fields.Selection([('1','Negative'),('2','Positive')],'Nitrite')
    ure_leucocytes = fields.Selection([('0','Negative'),('1','+'),('2','++'),('3','+++'),('4','+/-')],'Leucocytes')
    ure_glucose = fields.Selection([('0','Negative'),('1','+'),('2','++'),('3','+++'),('4','++++')],'Glucose')
    ure_specificgravity = fields.Selection([('0','1.000'),('1','1.005'),('2','1.010'),('3','1.015'),('4','1.020'),('5','1.025'),('6','1.030')],'Specific Gravity')
    ure_ph = fields.Selection([('0','5.0'),('1','6.0'),('2','6.5'),('3','7.0'), ('4','7.5'),('5','8.0'),('6','8.5')],'pH')

    #Urine Microscopy Section
    um_rbc = fields.Char('Urine RBC')
    um_wbc = fields.Char('Urine Pus Cells')
    um_crystals = fields.Char('Urine Crystals')
    um_epithelial = fields.Char('Epithelial Cells')
    um_misc = fields.Char('Miscellaneous')
    um_bacteria = fields.Char('Bacterial')
    um_appearance = fields.Char('Appearance')
    um_casts = fields.Char('Casts')

    #misc results
    bleedingTime_results = fields.Char('Bleeding Time')
    clottingTime_results = fields.Char('Clotting Time')

class miscresults(models.Model):
    _name='lab.miscresults'
    name = fields.Char('Name of the Investigation')
    units = fields.Char('Units')
    range = fields.Char('Range')
    result = fields.Char('Results')
    labno = fields.Char('Lab Number')
    labvisit=fields.Many2one('lab.labvisit')

class visitresults(models.Model):
    _name = 'lab.visitresults'
    labvisit = fields.Many2one('lab.labvisit')
    name = fields.Char('Name of the Investigation')
    units = fields.Char('Units')
    range = fields.Char('Reference Range')
    result = fields.Char('Result')
    labno = fields.Char('Lab Number')
    sequence = fields.Char('Sequence')


class lab_investigations(models.Model):
    _name = 'lab.investigations'
    _description = 'Biochemistry Order Module'
    labno = fields.Char('Lab Number')
    labvisit = fields.Many2one('lab.labvisit')



class biochemresults(models.Model):
    _name = 'lab.biochemresults'
    labvisit = fields.Many2one('lab.labvisit')
    name = fields.Char('Name of the Investigation')
    units = fields.Char('Units')
    range = fields.Char('Reference Range')
    result = fields.Char('Result')
    labno = fields.Char('Lab Number')




