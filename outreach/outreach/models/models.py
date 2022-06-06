# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from io import BytesIO, StringIO
import xlwt
import base64
from dateutil.relativedelta import relativedelta


import logging

_logger = logging.getLogger(__name__)


class outreach(models.Model):
    _name = 'outreach.outreach'
    _rec_name = 'dateclinic'
    dateclinic = fields.Date('Date of Clinic', default=fields.Date.today)
    appts = fields.One2many('outreach.records', 'outreach')
    file = fields.Binary('XLS File', readonly=True)
    filename = fields.Char('Name')


    @api.multi
    def get_data(self):
        for record in self:
            _logger.info('Button for getting values')
            datetouse = record.dateclinic
            datestart = datetouse.strftime(DATE_FORMAT)
            dateend = datetouse.strftime(DATE_FORMAT)
            datestart += " 00:00:01"
            dateend += " 23:59:59"
            orders = self.env['pos.order'].search([['date_order', '>=', datestart], ['date_order', '<=', dateend]])
            for order in orders:
                record.appts = [(0, 0, {'patient': order.partner_id, 'dateclinic':record.dateclinic})]

    @api.multi
    def exportcsv(self):
        fp = BytesIO()
        workbook = xlwt.Workbook(encoding='utf-8')
        writer = workbook.add_sheet('Outreach', cell_overwrite_ok=True)
        style_bold = "font: bold on"
        style_normal = "font: bold off"
        bold = xlwt.easyxf(style_bold)
        normal = xlwt.easyxf(style_normal)
        row = 0
        column = 0
        for x in range(10):
            writer.col(x).width = 256 * 20
        writer.write(row, column, "Serial No.", bold)
        writer.write(row, column + 1, "Date", bold)
        writer.write(row, column + 2, "ID", bold)
        writer.write(row, column + 3, "Age", bold)

        for record in self:
            for appt in record.appts:
                column = 0
                row += 1
                writer.write(row, column, row, normal)
                writer.write(row, column + 1, record.dateclinic.strftime(DATE_FORMAT), normal)
                writer.write(row, column + 2, appt.patient.name, normal)
                writer.write(row, column + 3, appt.patient.agecal, normal)

        workbook.save(fp)
        self.file = base64.b64encode(fp.getvalue())
        self.filename = self.id

        return {
            'name': 'Outreach Data',
            'type': 'ir.actions.act_url',
            'url': '/web/content/outreach.outreach/%s/file/outreach.xls?download=true' % (self.id),
            'target': 'new',
        }


class outreachrecords(models.Model):
    _name = 'outreach.records'
    _rec_name = 'patient'
    patient = fields.Many2one('res.partner', string='Patient name')
    outreach = fields.Many2one('outreach.outreach')
    dob = fields.Date(related='patient.dob')
    dateclinic = fields.Date(default=fields.Date.today)
    agecal = fields.Integer(compute='_age')

    @api.depends('dob', 'dateclinic')
    def _age(self):
        for record in self:
            if record.dob:
                dt = str(record.dob)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = record.dateclinic
                record.agecal = relativedelta(d2, d1).years




class clinicdetails(models.Model):
    _name = 'outreach.clinicdetails'
    _rec_name = 'patient'
    patient = fields.Many2one('res.partner')
    age = fields.Integer('Age')
    dateclinic = fields.Date('Date of Clinic')
    registration = fields.Char(related='patient.registration')    
