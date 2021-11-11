# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,date
from dateutil.relativedelta import relativedelta


class endoscopy(models.Model):
    _name = 'endoscopy.endoscopy'
    _description = 'Module for endoscopy reporting'
    _rec_name = 'partner_id'
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    date = fields.Date('Date', default=fields.Date.today())
    registration = fields.Char(related='partner_id.registration')
    dob = fields.Date(related='partner_id.dob')
    agecal = fields.Integer(compute='_age', store=True, group_operator=False)
    gender = fields.Selection(related='partner_id.gender')
    images=fields.One2many('endoscopy.images','endoscopy', string ='Images' )
    findings = fields.Text('Endoscopy Findings')
    impression = fields.Char('Impression')
    study = fields.Selection([('nasal','Nasal Endoscopy'),('laryngoscopy','Laryngoscopy')])

    @api.depends('dob', 'date')
    def _age(self):
        for record in self:
            if record.dob:
                dt = str(record.dob)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = record.date
                record.agecal = relativedelta(d2, d1).years


class endoscopyimages(models.Model):
    _name='endoscopy.images'
    _rec_name='caption'
    caption = fields.Char('Caption')
    image = fields.Binary('Image')
    endoscopy = fields.Many2one('endoscopy.endoscopy', ondelete='cascade')


class allergytest(models.Model):
    _name = 'endoscopy.allergytest'
    _rec_name ='partner_id'
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    date = fields.Date('Date', default=fields.Date.today())
    registration = fields.Char(related='partner_id.registration')
    dob = fields.Date(related='partner_id.dob')
    agecal = fields.Integer(compute='_age', store=True, group_operator=False)
    gender = fields.Selection(related='partner_id.gender')
    start_time = fields.Float('Start Time')
    end_time = fields.Float('End Time')
    ordered_by=fields.Char('Ordered By')
    complaints = fields.Char('Presenting Complaints')
    saline_wheal = fields.Float('Saline')
    saline_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    dfarina_wheal = fields.Float('Dermatophagoids farina')
    dfarina_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    dperonysinus_wheal = fields.Float('Dermatophagoids pteronysinus Wheal Diameter')
    dperonysinus_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    btropicalis_wheal = fields.Float('Blomia tropicalis')
    btropicalis_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    aconyzoides_wheal = fields.Float('Ageratum conyzoides')
    aconyzoides_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    aspinosus_wheal = fields.Float('Amaranthus spinosus')
    aspinosus_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    amexicana_wheal = fields.Float('Argemone mexicana')
    amexicana_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    aindica_wheal = fields.Float('Azadirechta indica')
    aindica_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    bnigra_wheal = fields.Float('Brassica nigra Wheal Diameter')
    bnigra_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    cpapaya_wheal = fields.Float('Carica papaya')
    cpapaya_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    cdactylon_wheal = fields.Float('Cynodon dactylon')
    cdactylon_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    crotundus_wheal = fields.Float('Cyperus rotundus')
    crotundus_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    eucalyptus_wheal = fields.Float('Eucalyptus sp')
    eucalyptus_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    hintegrifolia_wheal = fields.Float('Holoptelea integrifolia')
    hintegrifolia_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    xstrumarium_wheal = fields.Float('Xanthium strumarium')
    strumarium_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    zmays_wheal = fields.Float('Zea mays')
    mays_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    alternata_wheal = fields.Float('Alternaria alternata')
    alternata_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    afumigatus_wheal = fields.Float('Aspergillus fumigatus')
    fumigatus_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    aniger_wheal = fields.Float('Aspergillus niger')
    niger_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    rnigricans_wheal = fields.Float('Rhizopus nigricans')
    nigricans_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    cherbarum_wheal = fields.Float('Cladosporium herbarum')
    herbarum_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    fsolanii_wheal = fields.Float('Fusarium solanii')
    solanii_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    helminthosporium_wheal = fields.Float('Helminthosporium sp')
    helminthosporium_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    cockroach_wheal = fields.Float('Cockroach')
    cockroach_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    house_wheal = fields.Float('House dust')
    house_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    cat_wheal = fields.Float('Cat epithelia')
    cat_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    dog_wheal = fields.Float('Dog epithelia')
    dog_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    hdihydrochloride_wheal = fields.Float('Histamine dihydrochloride')
    dihydrochloride_interpretation = fields.Selection([('neg','Negative'),('one','+'),('two','++'),('three','+++')],'',default='neg')
    impression = fields.Char('Impression')

    @api.depends('dob', 'date')
    def _age(self):
        for record in self:
            if record.dob:
                dt = str(record.dob)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = record.date
                record.agecal = relativedelta(d2, d1).years

