# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)


class wizard(models.TransientModel):
    _name = 'sankerdaily.printdaily'
    datestart = fields.Date('Start Date')
    dateend = fields.Date('End Date')

    @api.multi
    def get_report(self):
        _logger.info(self.datestart)
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'datestart': self.datestart,
                'dateend': self.dateend,
            },
        }
        return self.env.ref('sankerdaily.printdaily_report').report_action(self, data=data)


class printdaily(models.AbstractModel):
    _name = 'report.sankerdaily.sankerprintdailytakings'

    @api.model
    def _get_report_values(self, docids, data=None):
        datestart = data['form']['datestart']
        dateend = data['form']['dateend']
        _logger.info(data['form']['datestart'])
        _logger.info(dateend)

        docs = []
        appts = self.env['sankerdaily.dailytakings'].search([['date', '>=', datestart], ['date', '<=', dateend]])
        
        for appt in appts:
            docs.append({
                'date': appt.date,
                'consulttotal': appt.consulttotal,
                'consultfree': appt.consultfree,
                'consultbalance': appt.consultbalance,
                'consultreal': appt.consultreal,
                'consultnet': appt.consultnet,
                'medtotal': appt.medtotal,
                'medfree': appt.medfree,
                'medbalance': appt.medbalance,
                'medreal': appt.medreal,
                'mednet': appt.mednet,
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'datestart': datestart,
            'dateend': dateend,
            'docs': docs,
        }


class consultrecord(models.TransientModel):
    _name = 'sankerdaily.consultrecord'
    datestart = fields.Date('Start Date')
    dateend = fields.Date('End Date')

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'datestart': self.datestart,
                'dateend': self.dateend,
            },
        }
        return self.env.ref('sankerdaily.consultrecord_report').report_action(self, data=data)



class consultrecordprint(models.AbstractModel):
    _name = 'report.sankerdaily.sankerconsultrecord'

    @api.model
    def _get_report_values(self, docids, data=None):
        datestart = data['form']['datestart']
        dateend = data['form']['dateend']

        docs = []
        appts = self.env['sankerdaily.dailytakings'].search([['date', '>=', datestart], ['date', '<=', dateend]])
        
        for appt in appts:
            docs.append({
                'date': appt.date,
                'eddie': appt.eddie,
                'eddiedue': appt.eddiedue,
                'didak': appt.didak,
                'didakdue': appt.didakdue,
                'slahiri': appt.slahiri,
                'slahiridue': appt.slahiridue,
                'vranee': appt.vranee,
                'vraneedue': appt.vraneedue,
                'gideon': appt.gideon,
                'eeg': appt.eeg,
                'gideondue': appt.gideondue,
        })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'datestart': datestart,
            'dateend': dateend,
            'docs': docs,
        }

