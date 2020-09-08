# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from io import BytesIO, StringIO
import xlwt
import base64
import logging
_logger = logging.getLogger(__name__)



class wizard(models.TransientModel):
    _name = 'opregistration.pharmacyexcel'
    dateselect = fields.Datetime()
    dateend = fields.Datetime()
    datetest = fields.Date('Select date')
    file = fields.Binary('XLS File', readonly=True)
    filename = fields.Char('Name')

    @api.onchange('datetest')
    def datecalc(self):
        for record in self:
            if record.datetest:
                date_touse = record.datetest - timedelta(days=1)
                date_str = date_touse.strftime('%d/%m/%Y')
                date_to = record.datetest.strftime('%d/%m/%Y')
                date_str += "18,30"
                date_to += "18,30"
                record.dateselect = datetime.strptime(date_str, '%d/%m/%Y%H,%M')
                record.dateend = datetime.strptime(date_to, '%d/%m/%Y%H,%M')
                _logger.info('onchange')
                _logger.info(self.dateend)

    @api.multi
    def get_excel_report(self):
        fp = BytesIO()
        workbook = xlwt.Workbook(encoding='utf-8')
        writer = workbook.add_sheet('Pharmacy Daily', cell_overwrite_ok=True)
        style_bold = "font: bold on"
        style_normal = "font: bold off"
        bold = xlwt.easyxf(style_bold)
        normal =xlwt.easyxf(style_normal)
        row=0
        column=0
        writer.write(row, column, "Serial No.", bold)
        writer.write(row, column+1, "Patient", bold)
        writer.write(row, column+2, "Consultation", bold)
        writer.write(row, column+3, "Medicines", bold)
        writer.write(row, column+4, "Total", bold)
        writer.write(row, column+5, "Balance", bold)
        writer.write(row, column+6, "Amount Paid", bold)
        consult_total = 0
        medicines_total = 0
        balance_total = 0
        paid_total = 0
        total_total = 0

        appts  = self.env['pos.order'].search([['date_order','>=',self.dateselect],['date_order','<=',self.dateend], ['config_id.name', '=', 'Pharmacy']], order='create_date')

        for appt in appts:
            consultation = 0
            medicines = 0
            balance =0
            paid = 0
            column = 0
            row +=1
            for appt.line in appt.lines:
                if appt.line.product_id.display_name == 'Consultation Fee':
                    consultation = appt.line.price_subtotal_incl
            medicines = appt.amount_total - consultation
            for appt.statement_id in appt.statement_ids:
                if appt.statement_id.journal_id.name == 'Credits':
                    balance = appt.statement_id.amount
            paid = appt.amount_total - balance
            consult_total += consultation
            medicines_total += medicines
            balance_total += balance
            paid_total += paid
            total_total += appt.amount_total
            writer.write(row, column, row, normal)
            writer.write(row, column + 1, appt.partner_id.name, normal)
            writer.write(row, column + 2,  consultation, normal)
            writer.write(row, column + 3, medicines, normal)
            writer.write(row, column + 4, appt.amount_total, normal)
            writer.write(row, column + 5, balance, normal)
            writer.write(row, column + 6, paid, normal)
        writer.write(row+1, column, "Total", bold)
        writer.write(row+1, column+1, "", bold)
        writer.write(row+1, column+2, consult_total, bold)
        writer.write(row+1, column+3, medicines_total, bold)
        writer.write(row+1, column+4, total_total, bold)
        writer.write(row+1, column+5, balance_total, bold)
        writer.write(row+1, column+6, paid_total, bold)


        workbook.save(fp)
        self.file=base64.b64encode(fp.getvalue())
        self.filename=self.id
        return {
                'name': 'Pharmacy Excel Report',
                'type': 'ir.actions.act_url',
                'url': '/web/content/opregistration.pharmacyexcel/%s/file/filename.xlsx?download=true' %(self.id),
                'target': 'new',
            }



