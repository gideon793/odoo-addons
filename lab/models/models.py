# -*- coding: utf-8 -*-
from typing import List, Tuple

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging
import json
import urllib.request

_logger = logging.getLogger(__name__)

class lab_investigations(models.Model):
    _name = 'lab.investigations'
    _rec_name = 'name'
    name = fields.Char('Name of the Investigation')
    range = fields.Char('Reference Range')
    group = fields.Many2one('lab.investigation_groups')
    rate = fields.Float('Rate')
    machine = fields.Selection([('biochem','Biochemistry'),('hematology','Hematology')])



class investigationgroups(models.Model):
    _name = 'lab.investigation_groups'
    _rec_name = 'name'
    name = fields.Char('Investigation Group')
    investigations = fields.One2many('lab.investigations', 'group', 'Investigations')


class labvisit(models.Model):
    _name = 'lab.labvisit'
    _rec_name='labno'
    partner_id = fields.Many2one('res.partner')
    labno=fields.Char('LabNo', readonly=True, required=True, copy=False, default='New')
    date = fields.Date(string='Date of Appointment', default=fields.Date.today())
    registration = fields.Char(related='partner_id.registration', store=True)
    dob = fields.Date(related='partner_id.dob')
    agecal = fields.Integer(compute='_age', store=True, group_operator=False)
    address = fields.Char(related='partner_id.contact_address')
    gender = fields.Selection(related='partner_id.gender')
    doctor = fields.Selection([('ssyiem', 'Dr. S. Syiem'), ('eddie', 'Dr. E. Mukhim'), ('didak', 'Dr. D. Khonglah'),
                               ('gideon', 'Dr. G. Rynjah'), ('rlaloo', 'Dr. R. Laloo'),
                               ('lashngain', 'Dr.  L. Sohliya'), ('dkynjin', 'Dr. D. Kynjin'),
                               ('self', 'Self'), ('other', 'Other')], string='Doctor')
    group_invs = fields.One2many('lab.visitgroupinvestigations','labvisit', string='Investigation Groups')
    investigations = fields.One2many('lab.visitinvestigations', 'labvisit', string='Investigations')

    @api.depends('dob', 'date')
    def _age(self):
        for record in self:
            if record.dob:
                dt = str(record.dob)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = record.date
                record.agecal = relativedelta(d2, d1).years

    @api.multi
    def getinvestigations(self):
        inv= []
        for each in self.group_invs:
            for ever in each.groups.investigations:
                inv.append((0,0,{'investigations': ever}))
        self.investigations = inv

    @api.model
    def create(self, vals):
        if vals.get('labno', 'New') == 'New':
            vals['labno'] = self.env['ir.sequence'].next_by_code('lab.labvisit') or 'New'
        result = super(labvisit, self).create(vals)
        return result

    def _reset_token_number_sequences(self):
        # just use write directly on the result this will execute one update query
        sequences = self.env['ir.sequence'].search([('name', '=like', '%labvisit%')])
        sequences.write({'number_next_actual': 1}) 


class visitinvestigations(models.Model):
    _name = 'lab.visitinvestigations'
    labvisit = fields.Many2one('lab.labvisit')
    investigations = fields.Many2one('lab.investigations')
    _sql_constraints = [('investigations_constraints','UNIQUE (investigations)', 'Investigation already added. Please remove duplicates')]

class visitgroupinvestigations(models.Model):
    _name = 'lab.visitgroupinvestigations'
    labvisit = fields.Many2one('lab.labvisit')
    groups = fields.Many2one('lab.investigation_groups')