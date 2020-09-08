# -*- coding: utf-8 -*-

from odoo import models, fields, api
from io import BytesIO
import base64




class ddrs(models.Model):
    _name = 'ddrs.ddrs'
    _description = 'DDRS Scheme'
    date = fields.Date('Transaction Date', required=True)
    name = fields.Char('Details')
    account = fields.Selection([('honorarium', 'Recurring - Honororium'), ('recurringother', 'Recurring - Non Honorarium'),
                                ('nonrecurring', 'Non-Recurring')])
    items = fields.Selection([('bamboo','Bamboo Processing Machines'),('wire','Wire, wood, barrels'),('furniture','Furniture, cots, mattresses'),('kitchen','Kitchen equipments'),
                               ('wood','Wood and Bamboo - recurring'), ('paper','Paper and Bleach - recurring'), ('maint','Building Maintenance'),('rent','Bed Rent'),('medicine','Medicines'),('food','Food'),('contingency','COntingency - clothing, toiletries, etc')])
    amount = fields.Float('Transaction Amount')
    attach = fields.Binary('Attachment', attachment=True)
    note = fields.Char('Notes')


class ddrsemployee(models.Model):
    _name = 'ddrs.ddrsemployee'
    _description = 'DDRS Employees'
    name= fields.Many2one('sankeremployee.sankeremployee', string='Employee Name')
    designation = fields.Char('Designation')
    honorarium = fields.Float('DDRS Honorarium')

class ddrsmonthly(models.Model):
    _name='ddrs.monthly'    
    _description = 'DDRS Monthly Salary Records'
    name = fields.Many2one('sankeremployee.sankeremployee', string='Employee name')
    honorariums = fields.Float('DDRS Honorarium')
    salaries = fields.Many2one('ddrs.ddrssalaries')
    month = fields.Char('Month')
    sequences = fields.Integer(string='Sequence', required=True, copy=False, default='000')



class ddrssalaries(models.Model):
    _name = 'ddrs.ddrssalaries'
    _description = 'DDRS Salaries'
    _rec_name='month'
    month = fields.Char('Month')
    transferdate = fields.Date('Date for Bank Transfer')
    entries = fields.One2many('ddrs.monthly', 'salaries', string='Salary Entries')        
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    salarydate = fields.Date('Date of Salary Record')
   
    @api.multi
    def textreport(self):
        debit = 0
        filedata = BytesIO()
        employees = self.entries
        for employee in employees:
            debit += employee.honorariums
        debitstr = str("%.2f" % debit)
        filedata.write(b"38481527209")
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
            filedata.write(bytes(employee.name.acctno, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(employee.name.branch, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(self.transferdate.strftime("%d/%m/%Y"), 'utf8'))
            filedata.write(b"#")
            netpayablestr = str("%.2f" % employee.honorariums)
            filedata.write(b"#")
            filedata.write(bytes(netpayablestr, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(self.month, 'utf8'))
            filedata.write(b"#")
            filedata.write(bytes(self.month, 'utf8'))
            filedata.write(b" salary#\n")

        values = {
            'name': "SBI_ddrs_upload.txt",
            'datas_fname': 'SBI_ddrs_upload.txt',
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
    def getsalaries(self):
        self.entries.unlink()
        staffs = self.env['ddrs.ddrsemployee'].search([])
        employees = []
        for staff in staffs:
            employees.append((0, 0, {'name': staff.name.id, 'honorariums': staff.honorarium,'month': self.month}))
        self.entries = employees



