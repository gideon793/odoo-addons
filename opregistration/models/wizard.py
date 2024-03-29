# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class wizard(models.TransientModel):
    _name='opregistration.wizard'
    dateselect = fields.Date('Date',required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'dateselect': self.dateselect,
            },
        }
        return self.env.ref('opregistration.opddaily_report').report_action(self, data=data)

class opdailyreport(models.AbstractModel):
    _name = 'report.opregistration.daily_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        dateselect=data['form']['dateselect']
        datetest=str(datetime.strptime(dateselect, DATE_FORMAT))
        docs = []
        appts  = self.env['opregistration'].search([['date','=',dateselect],'|',['type','=','old'],['type','=','new']], order='providerlink, type')
        for appt in appts:
            docs.append({
                'name': appt.partner_id.name,
                'registration': appt.registration,
                'type': appt.type,
                'age': appt.partner_id.agecal,
                'gender': appt.partner_id.gender,
                'doctor': appt.doctor,                
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'dateselect': dateselect,
            'docs': docs,
        }
