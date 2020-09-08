# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)


class wizard(models.TransientModel):
    _name = 'opregistration.projectreport'
    dateselect = fields.Datetime()
    dateend = fields.Datetime()
    datetest = fields.Date('Select date')
    point = fields.Selection([('Pharmacy', 'SAN-KER Pharmacy'), ('Outreach', 'Outreach'), ('Project', 'Mawkyrwat Project'), ('Nongstoin','Nongstoin Project'), ('Mairang','Mairang Project'),('Fatima','Fatima Project')], string='Location', default='Pharmacy')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)


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
                _logger.info(date_touse)
                _logger.info(date_str)
                _logger.info(date_to)
                record.dateselect = datetime.strptime(date_str, DATETIME_FORMAT)
                record.dateend = datetime.strptime(date_to, DATETIME_FORMAT)

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'dateselect': self.dateselect,
                'dateend': self.dateend,
                'point': self.point,
                'currency_id': self.currency_id

            },
        }
        return self.env.ref('opregistration.projectreport_report').report_action(self, data=data)


class opdailyreport(models.AbstractModel):
    _name = 'report.opregistration.projectreport'

    @api.model
    def _get_report_values(self, docids, data=None):
        dateselect = data['form']['dateselect']
        dateend = data['form']['dateend']
        point= data['form']['point']
        currency_id = data['form']['currency_id']
        docs = []
        appts = self.env['pos.order'].search([['date_order', '>=', dateselect], ['date_order', '<=', dateend], ['config_id.name', '=', point]], order='create_date')
        for appt in appts:
            _logger.info(appt.partner_id.name)
            _logger.info(appt.name)
            if appt.picking_id:
                lots = self.env['stock.move.line'].search([['picking_id', '=', appt.picking_id.id]])
            else:
                lots = ''
            for lot in lots:
                _logger.info(lot.lot_id)
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
            'point': point,
            'docs': docs,
            'currency_id': currency_id,

        }
