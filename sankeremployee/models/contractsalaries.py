# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import base64
import xlwt
_logger = logging.getLogger(__name__)
from io import BytesIO
import calendar
import datetime


class conractsalaries(models.Model):
    _name = 'sankeremployee.contractsalaries'
    _rec_name = 'month'
    month = fields.Char('Month')
    transferdate = fields.Date('Date for Bank Transfer')
    days = fields.Integer('Number of Days')
    workingday = fields.Date('Last Working Day of the Month')
    entries = fields.One2many('sankeremployee.contractmonthly', 'salaries', string='Salary Entries')
    salarydate = fields.Date('Date of Salary Record')


    @api.multi
    def textreport(self):
        debit = 0
        _logger.info('textreport')
        filedata = BytesIO()
        employees = self.entries
        for employee in employees:
            debit += employee.grossdue
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
        filedata.write(b" contractual payment")
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
            netpayablestr = str("%.2f" % employee.grossdue)
            filedata.write(b"#")
            filedata.write(bytes(netpayablestr, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(self.month, 'utf8'))
            filedata.write(b"contract")
            filedata.write(b"#")
            filedata.write(bytes(self.month, 'utf8'))
            filedata.write(b" contractual payment#\n")

        values = {
            'name': "SBI_contract_upload.txt",
            'datas_fname': 'SBI_contract_upload.txt',
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
            "url":  str(download_url),
            "target": "new",
        }



    @api.multi
    def getsalaries(self):
        self.entries.unlink()
        staffs = self.env['sankeremployee.contractemployee'].search([])
        employees = []
        for staff in staffs:
            employees.append((0,0,{'employee': staff.id, 'days': self.days, 'worked': self.days, 'grossdue': staff.grossdue, 'month': self.month, 'workingday': self.workingday, 'receipt_no': '0'}))
        self.entries = employees

