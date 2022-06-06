# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from io import BytesIO, StringIO
import xlwt
import base64
import logging
_logger = logging.getLogger(__name__)



class wizard(models.TransientModel):
    _name = 'opregistration.pharmacyexcel'
    dateselect = fields.Datetime()
    dateend = fields.Datetime()
    datetest = fields.Date('Select date', default = fields.Date.today ())
    file = fields.Binary('XLS File', readonly=True)
    filename = fields.Char('Name')
    point = fields.Selection([('Pharmacy', 'SAN-KER Pharmacy'), ('Outreach', 'Outreach'), ('Project', 'Mawkyrwat Project'),('Nongstoin','Nonstoin Project'),('Mairang','Mairang Project'),('Fatima','Fatima Project')], string='Location', default='Pharmacy')

    

    @api.onchange('datetest')
    def datecalc(self):
        for record in self:
            if record.datetest:
                date_str = record.datetest.strftime(DATE_FORMAT)
                date_to = record.datetest.strftime(DATE_FORMAT)
                date_str += " 00:00:00"
                date_to += " 23:59:59"
                record.dateselect = datetime.strptime(date_str, DATETIME_FORMAT)
                record.dateend = datetime.strptime(date_to, DATETIME_FORMAT)
                _logger.info(self.dateselect)
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
        for x in range(10):
            writer.col(x).width = 256 *20
        writer.write(row, column, "Serial No.", bold)
        writer.write(row, column+1, "Patient", bold)
        writer.write(row, column+2, "Consultation", bold)
        writer.write(row, column+3, "Registration", bold)
        writer.write(row, column+4, "Medicines", bold)
        writer.write(row, column+5, "Miscellaneous", bold)
        writer.write(row, column+6, "Total", bold)
        writer.write(row, column+7, "Balance", bold)
        writer.write(row, column+8, "Amount Paid", bold)
        writer.write(row, column+9, "Notes", bold)
        consult_total = 0
        medicines_total = 0
        balance_total = 0
        paid_total = 0
        total_total = 0
        service_total = 0
        registration_total = 0

        appts  = self.env['sale.order'].search([['date_order','>=',self.dateselect],['date_order','<=',self.dateend], ['user_id', '=', 8]], order='create_date')

        for appt in appts:
            consultation = 0
            registration = 0
            service = 0
            medicines = 0
            balance =0
            paid = 0
            roundoff = 0
            column = 0
            row +=1
            for appt.line in appt.order_line:
                if appt.line.product_id.display_name == 'Consultation Fee':
                    consultation = appt.line.price_total
                if appt.line.product_id.type == 'service':
                    service += appt.line.price_total
                if appt.line.product_id.display_name == 'Round off':
                    roundoff += appt.line.price_total
                if appt.line.product_id.display_name == 'Registration Fee':
                    registration += appt.line.price_total
            service = service - consultation - registration - roundoff
            service = round(service)
            medicines = appt.amount_total - consultation - service - registration
            balance = self.env['account.invoice'].search([['origin', '=', appt.name]]).residual
            paid = appt.amount_total - balance
            consult_total += consultation
            registration_total += registration
            medicines_total += medicines
            service_total += service
            balance_total += balance
            paid_total += paid
            total_total += appt.amount_total
            writer.write(row, column, row, normal)
            writer.write(row, column + 1, appt.partner_id.name, normal)
            writer.write(row, column + 2,  consultation, normal)
            writer.write(row, column + 3,  registration, normal)
            writer.write(row, column + 4, medicines, normal)
            writer.write(row, column + 5, service, normal)
            writer.write(row, column + 6, appt.amount_total, normal)
            writer.write(row, column + 7, balance, normal)
            writer.write(row, column + 8, paid, normal)
            if appt.remarks:
                writer.write(row, column + 9, appt.remarks, normal)
        writer.write(row+1, column, "Total", bold)
        writer.write(row+1, column+1, "", bold)
        writer.write(row+1, column+2, consult_total, bold)
        writer.write(row+1, column+3, registration_total, bold)
        writer.write(row+1, column+4, medicines_total, bold)
        writer.write(row+1, column+5, service_total, bold)
        writer.write(row+1, column+6, total_total, bold)
        writer.write(row+1, column+7, balance_total, bold)
        writer.write(row+1, column+8, paid_total, bold)


        workbook.save(fp)
        self.file=base64.b64encode(fp.getvalue())
        self.filename=self.id
        return {
                'name': 'Pharmacy Excel Report',
                'type': 'ir.actions.act_url',
                'url': '/web/content/opregistration.pharmacyexcel/%s/file/dailypharmacy.xls?download=true' %(self.id),
                'target': 'new',
            }



