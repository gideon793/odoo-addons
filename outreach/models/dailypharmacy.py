# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)

 

class wizard(models.TransientModel):
    _name='opregistration.pharmacydaily'
    dateselect = fields.Datetime()
    dateend = fields.Datetime()
    datetest = fields.Date('Select date', default=fields.Date.today)
    
    @api.onchange('datetest')
    def datecalc(self):
        for record in self:
            if record.datetest:
                date_touse = record.datetest
                _logger.info(record.datetest)
                date_str = date_touse.strftime(DATE_FORMAT)
                date_to = record.datetest.strftime(DATE_FORMAT)
                date_str += " 00:00:01"
                date_to += " 23:59:59"
                record.dateselect = datetime.strptime(date_str, DATETIME_FORMAT)
                record.dateend = datetime.strptime(date_to, DATETIME_FORMAT)


    @api.multi
    def get_report(self):
        _logger.info(self.dateselect)
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'dateselect': self.dateselect,
                'dateend': self.dateend,
            },
        }
        return self.env.ref('opregistration.pharmacydaily_report').report_action(self, data=data)

class opdailyreport(models.AbstractModel):
    _name = 'report.opregistration.pharmacydaily'

    @api.model
    def _get_report_values(self, docids, data=None):
        dateselect=data['form']['dateselect']
        dateend=data['form']['dateend']
        docs = []
        appts  = self.env['pos.order'].search([['date_order','>=',dateselect],['date_order','<=',dateend],['config_id.name','!=','In Patient Sale']], order='create_date')
        for appt in appts:
            docs.append({
                'name': appt.partner_id.name,
                'registration': appt.partner_id.registration,
                'age': appt.partner_id.agecal,
                'lines':appt.lines,
                'total':appt.amount_total,
                'statement_ids':appt.statement_ids        
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'dateselect': dateselect,
            'dateend': dateend,
            'docs': docs,
        }
