# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import base64
import xlwt

_logger = logging.getLogger(__name__)
from io import BytesIO
import calendar
import datetime


class salaries(models.Model):
    _name = 'sankeremployee.salaries'
    _rec_name = 'month'
    month = fields.Char('Month')
    transferdate = fields.Date('Date for Bank Transfer')
    days = fields.Integer('Number of Days')
    entries = fields.One2many('sankeremployee.monthly', 'salaries', string='Salary Entries')
    epffile = fields.Binary('EPF Upload File')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    workingday = fields.Date('Last Working Day of the Month')
    salarydate = fields.Date('Date of Salary Record')

    @api.multi
    def textreport(self):
        debit = 0
        _logger.info('textreport')
        filedata = BytesIO()
        employees = self.entries
        for employee in employees:
            debit += employee.actualdue
        debitstr = str("%.2f" % debit)
        filedata.write(b"34898750924")
        filedata.write(b"#")
        filedata.write(b"04295")
        filedata.write(b"#")
        filedata.write(bytes(self.transferdate.strftime("%d/%m/%Y"), 'utf8'))
        filedata.write(b"#")
        filedata.write(bytes(debitstr, 'utf8'))
        filedata.write(b"#")
        filedata.write(b"#")
        filedata.write(bytes(self.month, 'utf8'))
        filedata.write(b"#")
        filedata.write(bytes(self.month, 'utf8'))
        filedata.write(b" salary#\n")
        for employee in employees:
            filedata.write(bytes(employee.employee.acctno, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(employee.employee.branch, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(self.transferdate.strftime("%d/%m/%Y"), 'utf8'))
            filedata.write(b"#")
            netpayablestr = str("%.2f" % employee.actualdue)
            filedata.write(b"#")
            filedata.write(bytes(netpayablestr, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(self.month, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(self.month, 'utf8'))
            filedata.write(b" salary#\n")

        values = {
            'name': "SBI_upload.txt",
            'datas_fname': 'SBI_upload.txt',
            'res_model': 'ir.ui.view',
            'res_id': False,
            'type': 'binary',
            'public': True,
            'datas': base64.b64encode(filedata.getvalue()),

        }
        attachment_id = self.env['ir.attachment'].sudo().create(values)
        download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
        return {
            "type": "ir.actions.act_url",
            "url": str(download_url),
            "target": "new",
        }

    @api.multi
    def epfreport(self):
        _logger.info('epfreport')
        epfr = BytesIO()
        employees = self.entries
        for employee in employees:
            if employee.employee.isepf == 1:
                epfr.write(bytes(employee.employee.epfno, 'utf8'))
                epfr.write(b"#~#")
                epfr.write(bytes(employee.employee.epfname, 'utf8'))
                epfr.write(b"#~#")
                basicstr = str("%.0f" % employee.employee.epfwage)
                basestr = str("%.0f" % employee.employee.basicpay)
                epfr.write(bytes(basestr, 'utf8'))
                epfr.write(b"#~#")
                epfr.write(bytes(basicstr, 'utf8'))
                epfr.write(b"#~#")
                epfr.write(bytes(basicstr, 'utf8'))
                epfr.write(b"#~#")
                epfr.write(bytes(basicstr, 'utf8'))
                epfr.write(b"#~#")
                epfc = str("%.0f" % employee.epfc)
                epfr.write(bytes(epfc, 'utf8'))
                epfr.write(b"#~#")
                eps = employee.employee.epfwage * 0.0833
                epsstr = str("%.0f" % eps)
                epfr.write(bytes(epsstr, 'utf8'))
                epfr.write(b"#~#")
                edli = employee.employee.epfwage * 0.0367
                edlistr = str("%.0f" % edli)
                epfr.write(bytes(edlistr, 'utf8'))
                epfr.write(b"#~#")
                epfr.write(b"0")
                epfr.write(b"#~#")
                epfr.write(b"0")
                epfr.write(b"\n")

        uploads = {
            'name': "EPF_upload.txt",
            'datas_fname': 'EPF_upload.txt',
            'res_model': 'ir.ui.view',
            'res_id': False,
            'type': 'binary',
            'public': True,
            'datas': base64.b64encode(epfr.getvalue()),

        }
        attachment_id = self.env['ir.attachment'].sudo().create(uploads)
        download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
        return {
            "type": "ir.actions.act_url",
            "url": str(download_url),
            "target": "new",
        }

    @api.multi
    def esicreport(self):
        _logger.info('esicreport')
        fp = BytesIO()
        workbook = xlwt.Workbook(encoding='utf-8')
        writer = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
        extxt = xlwt.easyxf(num_format_str="@")
        uploads = self.entries
        row = 0
        column = 0
        date = self.workingday
        dateupload = datetime.datetime(date.year, date.month, calendar.mdays[date.month])
        dateupload_str = dateupload.strftime('%d/%m/%Y')        
        writer.write(row, column, 'Esic Number', extxt)
        writer.write(row, column + 1, 'Name', extxt)
        writer.write(row, column + 2, 'No of working days', extxt)
        writer.write(row, column + 3, 'Esic Wage', extxt)
        writer.write(row, column + 4, '', extxt)
        writer.write(row, column + 5, 'Date', extxt)



        for upload in uploads:
            if upload.employee.isesic == 1:
                column = 0
                row += 1
                writer.write(row, column, upload.employee.esicno, extxt)
                writer.write(row, column + 1, upload.employee.esicname, extxt)
                writer.write(row, column + 2, upload.worked, extxt)
                writer.write(row, column + 3, upload.employee.esicwage, extxt)
                writer.write(row, column + 4, '', extxt)
                writer.write(row, column + 5, dateupload_str, extxt)
        workbook.save(fp)
        esicuploads = {
            'name': "ESIC_upload.xls",
            'datas_fname': 'ESIC_upload.xls',
            'res_model': 'ir.ui.view',
            'res_id': False,
            'type': 'binary',
            'public': True,
            'datas': base64.b64encode(fp.getvalue()),

        }
        attachment_id = self.env['ir.attachment'].sudo().create(esicuploads)
        download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
        return {
            "type": "ir.actions.act_url",
            "url": str(download_url),
            "target": "new",
        }

    @api.multi
    def getsalaries(self):
        self.entries.unlink()
        staffs = self.env['sankeremployee.sankeremployee'].search([['regular','=', 'True']])
        employees = []
        for staff in staffs:
            employees.append((0, 0, {'employee': staff.id, 'days': self.days,'basic':staff.basicpay, 'allowance': staff.allowance,
                                     'worked': self.days, 'professionaltax': staff.professionaltaxcalc,
                                     'special': staff.special, 'workingday': self.workingday, 'month': self.month}))
        self.entries = employees
