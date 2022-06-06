# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)


class wizard(models.TransientModel):
    _name = 'opregistration.nongstoinreport'
    dateselect = fields.Datetime()
    dateend = fields.Datetime()
    datetest = fields.Date('Select date')

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
            },
        }
        return self.env.ref('opregistration.nongstoinreport_report').report_action(self, data=data)


class opdailyreport(models.AbstractModel):
    _name = 'report.opregistration.nongstoinreport'

    @api.model
    def _get_report_values(self, docids, data=None):
        dateselect = data['form']['dateselect']
        dateend = data['form']['dateend']
        docs = []
        appts = self.env['pos.order'].search([['date_order', '>=', dateselect], ['date_order', '<=', dateend], ['config_id.name', '=', 'Nongstoin']],
                                             order='create_date')
        for appt in appts:
            _logger.info(appt.partner_id.name)
            lots = self.env['stock.move.line'].search([['picking_id', '=', appt.picking_id.id]])
            for lot in lots:
                _logger.info(lot.lot_id.life_date)
            docs.append({
                'name': appt.partner_id.name,
                'registration': appt.partner_id.registration,
                'age': appt.partner_id.agecal,
                'lines': appt.lines,
                'total': appt.amount_total,
                'lots': lots
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'dateselect': dateselect,
            'dateend': dateend,
            'docs': docs,
        }
