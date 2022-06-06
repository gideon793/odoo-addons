# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

 

class pharmacyregister(models.TransientModel):
    _name='opregistration.pharmacyregister'
    dateselect = fields.Datetime()
    dateend = fields.Datetime()
    datetest = fields.Date('Select date', default=fields.Date.today)
    point = fields.Selection([('Pharmacy', 'SAN-KER Pharmacy'),('Pharmacy 2','Pharmacy 2nd Counter'), ('Jowai', 'Jowai'), ('Mawkyrwat', 'Mawkyrwat Project'), ('Nongstoin','Nongstoin Project'), ('Mairang','Mairang Project'),('Fatima','Fatima Project'),('Laboratory','Laboratory')], string='Location', default='Pharmacy')

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


    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'dateselect': self.dateselect,
                'dateend': self.dateend,
                'point': self.point
            },
        }
        return self.env.ref('opregistration.pharmacyregister_report').report_action(self, data=data)

class pharmacyregister(models.AbstractModel):
    _name = 'report.opregistration.pharmacyregister'

    @api.model
    def _get_report_values(self, docids, data=None):
        dateselect=data['form']['dateselect']
        dateend=data['form']['dateend']
        point = data['form']['point']
        docs = []
        appts  = self.env['sale.order'].search([['date_order','>=',dateselect],['date_order','<=',dateend],['user_id','=',8]],order='create_date')
        for appt in appts:
            invoices = self.env['account.invoice'].search([['origin','=',appt.name]])
            docs.append({
                'name': appt.partner_id.name,
                'registration': appt.partner_id.registration,
                'age': appt.partner_id.agecal,
                'lines':appt.order_line,
                'total':appt.amount_total,
                'paid': (appt.amount_total - invoices.residual),
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'dateselect': dateselect,
            'dateend': dateend,
            'docs': docs,
        }
